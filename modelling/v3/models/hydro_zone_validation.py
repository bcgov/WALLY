import os
import json
import shap
import pandas as pd
import numpy as np
from xgboost import XGBRegressor, plot_importance, plot_tree
import xgboost as xgb
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from matplotlib import pyplot
import math
import itertools
from ast import literal_eval
from sklearn.model_selection import GridSearchCV, KFold
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import matplotlib.backends.backend_pdf
from minio import Minio
from zipfiles import zipdir
from minio_client import minio_client

BUCKET_NAME = 'modelling'
UPLOAD_TO_MINIO = False

# directory = '../data/training_data_hydro_zone_annual_flow/nov23/'
# directory = '../data/zones/'
# directory = '../data/zones_5percent/'
# directory = '../data/4_training/10_year_stations_by_zone_5_percent'
data_directory = '../data/4_training/jun17'
output_directory_base = "./output/jun17"
dependant_variable = 'mean'
zone_scores = {}
count = 0

# inputs = ["year","drainage_area","watershed_area","aspect","glacial_area","solar_exposure","potential_evapotranspiration_hamon",]  "annual_precipitation", 
# inputs = ["years_of_data","drainage_area","average_slope","annual_precipitation","glacial_coverage","potential_evapotranspiration","median_elevation","solar_exposure"]
inputs = ["drainage_area","average_slope","annual_precipitation","glacial_coverage","potential_evapotranspiration","median_elevation","solar_exposure"]

columns = list(inputs) + [dependant_variable]

show_error_plots = False

# params = {
#   'nthread':[6], #when use hyperthread, xgboost may become slower
#   'objective':['reg:squarederror'],
#   'learning_rate': [.03, 0.05, .07], #so called `eta` value
#   'max_depth': [5, 6, 7],
#   'min_child_weight': [4, 5, 6],
#   # 'subsample': [0.7, 0.85, 0.95],
#   'subsample': [0.7],
#   # 'colsample_bytree': [0.7, 0.85, 0.95],
#   'colsample_bytree': [0.7],
#   'n_estimators': [300]
# }

xgb_params = {
  'n_estimators': 1000,
  # 'eta': 0.001,
  # 'max_depth': 8,
  # 'min_child_weight': 2,
#   'subsample': 0.75,
#   'colsample_bytree': 0.95,
#   'colsample_bylevel': 0.95
}

model = XGBRegressor(**xgb_params, random_state=42)
# grid = GridSearchCV(estimator=model, param_grid=params, n_jobs=6, cv=folds, verbose=1, scoring='neg_root_mean_squared_error')

for filename in sorted(os.listdir(data_directory)):
    if filename.endswith(".csv"):
        best_r_squared = 0
        best_inputs = []
        # model = XGBRegressor(random_state=42)
        zone_name = filename.split('.')[0]
        print(type(zone_name))

        # DEBUG test for zone only
        if zone_name not in ["27"]:
            print("test")
            continue
        else:
            print("TRUE")

        # output_dir = "./output/annual_flow_model_analysis/zone_" + zone_name + "/"
        # output_dir = "./output/10_year_stations_analysis/xgboost/zone_" + zone_name + "/"

        output_dir = output_directory_base + "/zone_" + zone_name + "/"
        zone_df = pd.read_csv(os.path.join(data_directory, filename))

        # if this zone has less than # of data rows skip
        if len(zone_df.index) < 5:
            continue
        
        df_inputs =  list(inputs) + [dependant_variable]
        print(df_inputs)

        
        features_df = zone_df[df_inputs]

        # RANDOM DATA COLUMN
        # features_df['randNumCol'] = np.random.randint(1, 1000, features_df.shape[0])

        # X = features_df.dropna(subset=df_inputs) # drop NaNs
        X = features_df

        y = X[dependant_variable] # dependant
        X = X.drop([dependant_variable], axis=1) # independant
        mean_mar = round(y.mean(),4)

        # print(y)
        # print(X)

        if len(X.index) <=1:
            continue

        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

        all_models = []
        best_model = None
        fold_counter = 1
        
        folds = 5
        folds = min(folds, len(X.index))
        kf = KFold(n_splits=folds, random_state=None, shuffle=True)
        for train_index, test_index in kf.split(X):
            X_train, X_test = X.iloc[train_index,:], X.iloc[test_index,:]
            y_train, y_test = y.iloc[train_index].values.ravel(), y.iloc[test_index].values.ravel()

            eval_set = [(X_train, y_train), (X_test, y_test)]

            # grid.fit(X_train, y_train, eval_set=eval_set, eval_metric=["rmse", "logloss"], early_stopping_rounds=10)
            
            model.fit(X_train, y_train, eval_set=eval_set, eval_metric=["logloss", "rmse"], early_stopping_rounds=50)
            
            # DEBUG SETS TEST TO ALL DATA
            X_test = X
            y_test = y

            y_pred = model.predict(X_test)
            r2 = r2_score(y_test, y_pred) # model.score(X_test, y_test)
            rmse = mean_squared_error(y_test, y_pred, squared=False)
            results = model.evals_result()
            feat_import = model.feature_importances_

            # Report Figures Directory
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            pdf = matplotlib.backends.backend_pdf.PdfPages(output_dir + "fold_" + str(fold_counter) + "_stats.pdf")
            
            size = (10, 6)

            # Prediction vs real plot
            marker_size = 9
            fig_pred, ax1 = plt.subplots(figsize=size)
            # ax1.scatter(y_pred, y_test, label="Prediction", s=marker_size)
            ax1 = sns.regplot(y_pred, y_test, fit_reg=True, truncate=True) 
            # ax1.scatter(range(len(y_pred)), y_pred, label="Prediction", s=marker_size)
            # ax1.scatter(range(len(y_pred)), y_test, label="Real", s=marker_size)
            fig_pred.suptitle("Predicted MAR vs Real MAR")
            # Set x y plot axis limits
            xlim = ax1.get_xlim()[1]
            ylim = ax1.get_ylim()[1]
            max_size = max(xlim, ylim)
            # ax1.set_xlim([0, max_size])
            # ax1.set_ylim([0, max_size])
            ax1.set_xlabel('Pred MAR')
            ax1.set_ylabel('Real MAR')

            lx = np.linspace(0,max_size/2,100)
            ly = lx
            ax1.plot(lx, ly, ':')

            ax1.legend()
            pdf.savefig( fig_pred )
            # plt.show()

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

            # Feature Importance plot
            try:
                plt.rcParams["figure.figsize"] = size
                fig_importance_weight = plot_importance(model, importance_type='weight', title='weight').figure
                fig_importance_cover = plot_importance(model, importance_type='cover', title='cover').figure
                fig_importance_gain = plot_importance(model, importance_type='gain', title='gain').figure
                pdf.savefig( fig_importance_weight )
                pdf.savefig( fig_importance_cover )
                pdf.savefig( fig_importance_gain )

                shap_values = shap.TreeExplainer(model).shap_values(X)

                # summary plot
                fig_shap, ax_shap = plt.subplots(figsize=size)
                shap.summary_plot(shap_values, X, show=False)
                pdf.savefig( fig_shap )

                # fig_dep, ax_dep = plt.subplots(figsize=size)
                # shap.dependence_plot("glacial_coverage", shap_values, X, show=False)
                # pdf.savefig( fig_dep )

                # fig_tree = plot_tree(model, num_trees=4).figure
                # pdf.savefig( fig_tree )
                # fig_tree = xgb.to_graphviz(model, num_trees=0, rankdir='LR').figure
                # plt.show()
            except:
                print("ERROR IN FIG TREE")
                pass

            # Training Results plot
            epochs = len(results["validation_0"]["rmse"])
            x_axis = range(0, epochs)
            fig_results, ax = pyplot.subplots(figsize=size)
            ax.plot(x_axis, results["validation_0"]["rmse"], label="Train")
            ax.plot(x_axis, results["validation_1"]["rmse"], label="Test")
            ax.legend()
            txt = 'RMSE: ' + str(rmse) + ' R2: ' + str(r2)
            fig_results.suptitle(txt)
            pdf.savefig( fig_results )

            # Features vs Prediction plots
            for column in X_test.columns:
                fig_f, axf = plt.subplots(figsize=size)
                axf = sns.regplot(X_test[column], y_test, fit_reg=True)
                # axf.scatter(y_pred, X_test[column], s=marker_size)
                axf.set_xlabel(column)
                axf.set_ylabel('MAR')
                # axf.scatter(range(len(y_pred)), y_test, label="Real", s=marker_size)
                fig_f.suptitle(column + ' vs Predicted MAR')
                # axf.legend()
                pdf.savefig( fig_f )

                # fig_txt = plt.figure(figsize=size)
                # fig_txt.text(0.05,0.95, txt, transform=fig_txt.transFigure, size=12)
                # fig_txt.text(0.05,0.95, txt, transform=fig_txt.transFigure, size=12)
                # pdf.savefig( fig_txt )

            pdf.close()

            # plt.show()
            # fig.savefig(output_dir + "fold_" + str(fold_counter) + "_stats.png", bbox_inches='tight')
            # fip.figure.savefig(output_dir + "fold_" + str(fold_counter) + "_feature_importance.png", bbox_inches='tight')

            model_test = { 
                "model": model,
                "mean_mar": mean_mar,
                "r2": round(r2,4),
                "rmse": round(rmse,6),
                "results": results,
                "gain": feat_import,
                "fold": fold_counter
            }

            all_models.append(model_test)

            if best_model is None:
                best_model = model_test
            elif rmse < best_model['rmse']:
                best_model = model_test

            fold_counter += 1

        model = best_model['model']
        results = best_model['results']
        rmse = best_model['rmse']
        r2 = best_model['r2']
        mean_mar = best_model['mean_mar']

        r2s = []
        rmses = []
        foldsArr = []
        for item in all_models:
            # if item["r2"] > 0:
            r2s.append(item["r2"])
            rmses.append(item["rmse"])
            foldsArr.append(item["fold"])

        # rmses = [o.rmse for o in all_models]
        # r2s = all_models.map('r2')
        # rmses = all_models.map('rmse')


        fig1, (ax1, ax2, ax3) = pyplot.subplots(3, 1, figsize=(10,20))
        fig1.subplots_adjust(hspace=0.4)

        ax1.plot(r2s, rmses, 'o')
        ax1.set_xlabel("R2")
        ax1.set_ylabel("RMSE")
        ax1.title.set_text('RMSE vs R2')

        xrng = range(1,folds+1)

        ax2.plot(xrng, r2s, 'o')
        avg = sum(r2s) / len(r2s)
        ax2.plot(xrng, [avg] * len(xrng), ':')
        ax2.set_xlabel("FOLDS")
        ax2.set_ylabel("R2")
        ax2.title.set_text('Average R2')

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

        # Zip training report files together
        zip_filename = "zone_" + zone_name + ".zip"
        zipdir(output_dir, zip_filename)

        # Upload to minio
        minio_path = 'v1/training_reports/' + zip_filename
        local_path = "./" + zip_filename
        upload = minio_client.s3_upload_file(minio_path, local_path, 'zip', BUCKET_NAME)
        # results = grid.cv_results_
        # print(results)
        print("zone", zone_name)
        print("r2 score", r2)
        rmse = results["validation_1"]["rmse"][-1]
        rmse_95_p = rmse * 2
        print("RMSE 95%", rmse_95_p)

        if show_error_plots:
            epochs = len(results["validation_0"]["rmse"])
            x_axis = range(0, epochs)
            # plot rmse loss
            fig, ax = pyplot.subplots(figsize=(12,12))
            ax.plot(x_axis, results["validation_0"]["rmse"], label="Train")
            ax.plot(x_axis, results["validation_1"]["rmse"], label="Test")
            ax.legend()
            pyplot.ylabel("RMSE")
            pyplot.title("XGBoost RMSE")
            # plot log error
            # fig, ax = pyplot.subplots(figsize=(12,12))
            # ax.plot(x_axis, results["validation_0"]["logloss"], label="Train")
            # ax.plot(x_axis, results["validation_1"]["logloss"], label="Test")
            # ax.legend()
            # pyplot.ylabel("Log Error")
            # pyplot.title("XGBoost Log Error")

            plot_importance(model)
            pyplot.show()

        # raw_uncertainty = rmse / mean_mar
        # uncertainty = round(rmse / mean_mar, 4) * 100
        zone_name = filename.split('.')[0]
        json_filename = 'zone_' + zone_name + '.json'
        local_path = './output/model_state_files/' + json_filename
        model.save_model(local_path)
        # upload to minio
        minio_path = 'v1/hydro_zone_annual_flow/' + json_filename
        upload = minio_client.s3_upload_file(minio_path, local_path, 'json', BUCKET_NAME)

        zone_scores[zone_name] = {
          "R2": r2,
          "RMSE_68%": rmse,
          "RMSE_95%": rmse_95_p,
          # "MAR": mean_mar,
          # "+/-": str(uncertainty) + '%',
          # "raw": raw_uncertainty
        }

    else:
        continue

print()
print("Zone Model Results")
r2_sum = 0
rmse_sum = 0
rmse_95_sum = 0
for attr, value in zone_scores.items():
    print(attr, value)
    if not math.isnan(value["R2"]):
        r2_sum += value["R2"]
    if value["RMSE_68%"]:
        rmse_sum += value["RMSE_68%"]
    if value["RMSE_95%"]:
        rmse_95_sum += value["RMSE_95%"]

print("Score Totals for BC")
# print("R2", r2_sum)
print("RMSE_68%_Sum", rmse_sum)
print("RMSE_95%_Sum", rmse_95_sum)


with open('../model_output/hydro_zone_annual_flow/annual_model_scores.json', "w") as outfile:
    json.dump(zone_scores, outfile)
