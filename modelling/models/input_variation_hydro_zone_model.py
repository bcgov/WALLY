import os
import json
from numpy.core.numeric import allclose
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import math
import csv
import itertools
from ast import literal_eval
from sklearn.metrics import mean_squared_error, r2_score
from pathlib import Path
import matplotlib.backends.backend_pdf
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import pyplot
from operator import attrgetter
import pickle
from joblib import dump, load

# Model Settings
OUTPUT_DIR = 'Sept_9_2021'
TESTING_SIZE = 0.3
TEST_ALL_DATA = False
FOLDS = 50
DEPENDANT_VARIABLE = '7Q10-S'
NORMALIZE_LOWFLOW = True
ALLOCATED_THRESHOLD = 2
NET_THRESHOLD = 0
# ZONES = ["all_data"]
# ZONES = ["25", "26", "27", "all_data"]
ZONES = ["all_data"]
ALL_ZONES = False

directory = '../data/4_training/sept2_2021'
output_directory_base = "./output/" + OUTPUT_DIR
zone_scores = {}
count = 0

inputs_list = ["average_slope","annual_precipitation","glacial_coverage","potential_evapotranspiration","median_elevation","solar_exposure"]

all_combinations = []
for r in range(len(inputs_list) + 1):
    combinations_object = itertools.combinations(inputs_list, r)
    combinations_list = list(combinations_object)
    all_combinations += combinations_list

# limit input list size
all_combinations = [x for x in all_combinations if len(x)<=5]
print('total combinations: ', len(all_combinations))


def filter_data(df):
    return df[(df["percent_allocated_mad"] <= ALLOCATED_THRESHOLD) | (df["percent_allocated_mad_abs"] == NET_THRESHOLD)]


# 1. Find best performing inputs for each zone
for filename in sorted(os.listdir(directory)):
    if filename.endswith(".csv"):
        zone_name = filename.split('.')[0]

        # limits zones calculated if constant has zone numbers in it
        if zone_name in ZONES or ALL_ZONES:
            print("Starting Zone:", zone_name)
        else:
            continue
        
        model = LinearRegression()
        zone_df = pd.read_csv(os.path.join(directory, filename))
        zone_df = filter_data(zone_df)

        zone_df = zone_df.dropna(subset=[DEPENDANT_VARIABLE]) # drop NaNs
        print(zone_df)
        
        # Divide 7Q10-S by MAD
        if DEPENDANT_VARIABLE == '7Q10-S' and NORMALIZE_LOWFLOW:
            print('NORMALIZING LOWFLOW BY DIVIDING BY MAD')
            zone_df['7Q10-S'] = zone_df['7Q10-S'] / ((zone_df['mean'] / 1000) * zone_df['drainage_area'])
        
        print("ZONE DATA ROWS COUNT:", zone_df.shape)

        all_combo_stats = []

        local_dir = output_directory_base + "/zone_" + str(zone_name) + "/"
        Path(local_dir).mkdir(parents=True, exist_ok=True)

        for inputs in all_combinations:
            count += 1
            inputs = list(inputs) + [DEPENDANT_VARIABLE]
            # print(inputs)
            if len(inputs) < 2:
                continue
            features_df = zone_df[inputs]
            X = features_df.dropna(subset=[DEPENDANT_VARIABLE]) # drop NaNs
            y = X.get(DEPENDANT_VARIABLE) # dependant
            X = X.drop([DEPENDANT_VARIABLE], axis=1) # independant
            if len(X.index) <=1:
                continue
            
            best_r2 = 0
            min_r2 = 1
            all_r2 = []
        
            for i in range(0, FOLDS):
                if TEST_ALL_DATA:
                    model.fit(X, y)
                    X_test = X
                    y_test = y
                else:
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TESTING_SIZE)
                    model.fit(X_train, y_train)

                # model_score = model.score(X_test, y_test)
                r2 = model.score(X, y)

                y_pred = model.predict(X_test)
                correlation_matrix = np.corrcoef(y_test.to_numpy(), y_pred)
                correlation_xy = correlation_matrix[0,1]
                r2 = correlation_xy**2

                # print(r2)
                if r2 > best_r2:
                    best_r2 = r2
                if r2 < min_r2:
                    min_r2 = r2
                all_r2.append(r2)

            combo_stats = {
              "best_r2": best_r2,
              "min_r2": min_r2,
              "avg_r2": sum(all_r2) / len(all_r2),
              "columns": list(X.columns.values)
            }
            print(combo_stats)

            all_combo_stats.append(combo_stats)
        
        # Find best performing combo based on three factors
        highest_min_r2_combo = {'best_r2': 0, 'min_r2': 0, 'avg_r2': 0, 'columns': []}
        highest_best_r2_combo = {'best_r2': 0, 'min_r2': 0, 'avg_r2': 0, 'columns': []}
        highest_avg_r2_combo = {'best_r2': 0, 'min_r2': 0, 'avg_r2': 0, 'columns': []}
        for combo in all_combo_stats:
            if combo["best_r2"] == 0 or combo["min_r2"] == 1 or combo["avg_r2"] is math.nan:
                continue
            if combo["min_r2"] > highest_min_r2_combo["min_r2"]:
                highest_min_r2_combo = combo
            if combo["best_r2"] > highest_best_r2_combo["best_r2"]:
                highest_best_r2_combo = combo
            if combo["avg_r2"] > highest_avg_r2_combo["avg_r2"]:
                highest_avg_r2_combo = combo

        print("highest_min_r2_combo", highest_min_r2_combo)
        score = highest_min_r2_combo["min_r2"]
        best_inputs = highest_min_r2_combo["columns"]
        zone_scores[zone_name] = {
          "score": score,
          "best_inputs": best_inputs
        }

        # output all variation results file
        local_file_path = local_dir + "zone_" + str(zone_name) + "_input_variation_results.csv"
        df = pd.DataFrame(all_combo_stats)
        df.to_csv(local_file_path, index=False)

        print('ZONE:', zone_name, 'SCORE:', score, 'INPUTS:', best_inputs)
    else:
        continue


# 2. Run iterations on each zones best input set and output the summary
for attr, value in zone_scores.items():
    zone_name = 'zone_' + str(attr)
    zone_df = pd.read_csv(os.path.join(directory, str(attr) + '.csv'))
    zone_df = filter_data(zone_df)
    
    # Divide 7Q10-S by MAD
    if DEPENDANT_VARIABLE == '7Q10-S' and NORMALIZE_LOWFLOW:
        print('NORMALIZING LOWFLOW BY DIVIDING BY MAD')
        zone_df['7Q10-S'] = zone_df['7Q10-S'] / ((zone_df['mean'] / 1000) * zone_df['drainage_area'])

    print("2nd Round Size:", zone_df.shape)
    inputs = value["best_inputs"] + [DEPENDANT_VARIABLE]
    model = LinearRegression()
    features_df = zone_df[inputs + ['station_number']] 
    X = features_df.dropna(subset=[DEPENDANT_VARIABLE]) # drop NaNs
    y = X.get(DEPENDANT_VARIABLE) # dependant
    X = X.drop([DEPENDANT_VARIABLE], axis=1) # independant
    if len(X.index) <=1:
        continue

    fold_counter = 1
    all_models = []
    best_model = None
    
    fold_dir = local_dir + 'fold_data/'
    Path(fold_dir).mkdir(parents=True, exist_ok=True)

    for i in range(0, FOLDS):
        # Train Model
        if TEST_ALL_DATA:
            model.fit(X, y)
            X_test = X
            y_test = y
        else:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TESTING_SIZE)
            model.fit(X_train.drop(['station_number'], axis=1), y_train)

        y_pred = model.predict(X_test.drop(['station_number'], axis=1))
        # r2 = r2_score(y_test.to_numpy(), y_pred)
        r2_test = model.score(X_test.drop(['station_number'], axis=1), y_test)

        correlation_matrix = np.corrcoef(y_test.to_numpy(), y_pred)
        correlation_xy = correlation_matrix[0,1]
        r2 = correlation_xy**2

        print("")
        print("r2_test", r2_test, r2)
        print(fold_counter, r2)
        print(y_test.to_numpy())
        print(type(y_test.to_numpy())) 
        print(y_pred)
        print(type(y_pred))
        print("")
        
        rmse = mean_squared_error(y_test, y_pred, squared=False)
        
        X_test['y_test'] = y_test
        X_test['y_pred'] = y_pred
        X_test['r2'] = r2
        X_test['rmse'] = rmse

        fold_file_path = fold_dir + str(fold_counter) + '.csv'
        X_test_df = pd.DataFrame(X_test)
        try:
            print(fold_file_path)
            print(X_test_df)
            X_test_df.to_csv(fold_file_path, index=False)
            print("successfully exported fold data")
        except Exception as e:
            print("Error exporting fold data", e)
            

        feat_import = model.coef_
        intercept = model.intercept_
        output_dir = output_directory_base + "/zone_" + str(attr) + "/"

        # Report Output
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        pdf = matplotlib.backends.backend_pdf.PdfPages(output_dir + "fold_" + str(fold_counter) + "_stats.pdf")
        size = (10, 6)
        marker_size = 9
        # Pred MAR vs Real MAR
        fig_pred, ax1 = plt.subplots(figsize=size)
        ax1 = sns.regplot(y_pred, y_test, fit_reg=True, truncate=True) 
        fig_pred.suptitle("Predicted MAR vs Real MAR")
        xlim = ax1.get_xlim()[1]
        ylim = ax1.get_ylim()[1]
        max_size = max(xlim, ylim)
        ax1.set_xlabel('Pred MAR')
        ax1.set_ylabel('Real MAR')
        lx = np.linspace(0,max_size/2,100)
        ly = lx
        ax1.plot(lx, ly, ':')
        ax1.legend()
        pdf.savefig( fig_pred )
        # Covariance of Features
        corr = X.corr()
        corr.style.background_gradient(cmap='coolwarm')
        fig_cov, ax = plt.subplots(figsize=size)
        ax.set_xticks(range(len(corr.columns)))
        ax.set_yticks(range(len(corr.columns)))
        fig_cov.suptitle("Feature Correlations")
        ax = sns.heatmap(
            corr, 
            vmin=-1, vmax=1, center=0,
            cmap=sns.diverging_palette(20, 220, n=200),
            square=True
        )
        ax.set_xticklabels(
            ax.get_xticklabels(),
            rotation=45,
            horizontalalignment='right'
        )
        pdf.savefig( fig_cov )
        pdf.close()

        model_test = { 
            "model": model,
            "r2": round(r2,4),
            "rmse": round(rmse,6),
            "gain": feat_import,
            "fold": fold_counter
        }

        all_models.append(model_test)

        if best_model is None:
            best_model = model_test
        elif rmse < best_model['rmse']:
            best_model = model_test

        fold_counter += 1

    # Create summary reports
    model = best_model['model']
    rmse = best_model['rmse']
    r2 = best_model['r2']

    model_output_dir =output_directory_base + "/" + str(zone_name) + "/" + zone_name + '.joblib'
    dump(model, model_output_dir) 

    r2s = []
    rmses = []
    foldsArr = []
    for item in all_models:
        # if item["r2"] > 0:
        r2s.append(item["r2"])
        rmses.append(item["rmse"])
        foldsArr.append(item["fold"])

    fig1, (ax1, ax2, ax3) = pyplot.subplots(3, 1, figsize=(10,20))
    fig1.subplots_adjust(hspace=0.4)

    ax1.plot(r2s, rmses, 'o')
    ax1.set_xlabel("R2")
    ax1.set_ylabel("RMSE")
    ax1.title.set_text('RMSE vs R2')

    xrng = range(1, FOLDS + 1)

    ax2.plot(xrng, r2s, 'o')
    avg = sum(r2s) / len(r2s)
    ax2.plot(xrng, [avg] * len(xrng), ':')
    ax2.set_xlabel("FOLDS")
    ax2.set_ylabel("R2")
    ax2.title.set_text('Average R2')
    ax2.set_ylim([min(avg - 0.05, -1),1])

    ax3.plot(xrng, rmses, 'o')
    avg = sum(rmses) / len(rmses)
    ax3.plot(xrng, [avg] * len(xrng), ':')
    ax3.set_xlabel("FOLDS")
    ax3.set_ylabel("RMSE")
    ax3.title.set_text('Average RMSE')
    for i, fold in enumerate(foldsArr):
        ax1.annotate(str(fold), (r2s[i], rmses[i]))
    # pyplot.show()

    local_img_path = output_dir + zone_name + "_summary.png"
    fig1.savefig(local_img_path, bbox_inches='tight')

    print("zone", zone_name)
    print("r2 score", r2)
    rmse_95_p = rmse * 2
    print("RMSE 95%", rmse_95_p)


