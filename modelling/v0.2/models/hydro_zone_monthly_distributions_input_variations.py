import os
import json
import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
import math
import itertools

parent_directory = '../data/training_data_hydro_zone_monthly_distributions/nov23'
save_directory = '../model_output/hydro_zone_monthly_distributions/nov23'
dependant_variable = 'monthly_mean'

inputs_list = ["year","drainage_area","average_slope","glacial_coverage","glacial_area","watershed_area","potential_evapotranspiration_thornthwaite","potential_evapotranspiration_hamon","hydrological_zone","annual_precipitation","median_elevation","aspect","solar_exposure"]
# inputs_list = ["drainage_area", "average_slope", "glacial_coverage", "glacial_area", "annual_precipitation", "median_elevation", "potential_evapotranspiration_thornthwaite", "aspect", "solar_exposure"]
inputs_list = ["year", "drainage_area", "glacial_coverage", "glacial_area", "annual_precipitation", "potential_evapotranspiration_thornthwaite"]

all_combinations = []
for r in range(len(inputs_list) + 1):
    combinations_object = itertools.combinations(inputs_list, r)
    combinations_list = list(combinations_object)
    all_combinations += combinations_list

# limit input list size
all_combinations = [x for x in all_combinations if len(x)<=5]

print('total combinations: ', len(all_combinations))

for zone in range(1, 30): # zones
    zone_name = 'zone_' + str(zone)
    month_scores = {}
    for month in range(1, 13): # months
        best_r_squared = 0
        best_inputs = []
        xgb = XGBRegressor(random_state=42)
        file_path = parent_directory + '/' + zone_name + '/' + str(month) + '.csv'
        zone_df = pd.read_csv(file_path)

        for inputs in all_combinations:
            inputs = list(inputs) + [dependant_variable]
            if len(inputs) < 2:
                continue

            features_df = zone_df[inputs]
            X = features_df.dropna(subset=inputs) # drop NaNs

            y = X.get(dependant_variable) # dependant
            X = X.drop([dependant_variable], axis=1) # independant

            if len(X.index) <=1:
                continue

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)
            xgb.fit(X_train, y_train)
            xgb_score = xgb.score(X_test, y_test)

            if xgb_score > best_r_squared:
                best_r_squared = xgb_score
                best_inputs = list(X.columns.values)
                # print(best_r_squared)
                # print(best_inputs)
                print('Found New Best:', best_r_squared, best_inputs)

                month = str(month)
                outdir = save_directory + '/zone_{}'.format(zone)
                if not os.path.exists(outdir):
                    os.mkdir(outdir)
                outname = '{}.json'.format(month)
                save_path = os.path.join(outdir, outname)
                xgb.save_model(save_path)
                # save_path = save_directory + '/' + zone_name + '/' + month + '.json'
                # xgb.save_model('../model_output/hydro_zone_annual_flow/nov23/zone_{}.json'.format(zone_name))

            # save model output state
            # month = str(month)
            # save_directory = '../model_output/hydro_zone_monthly_distributions'
            # save_path = save_directory + '/' + zone_name + '/' + month + '.json'
            # xgb.save_model(save_path)

        # print score value
        score = round(best_r_squared, 5)
        month_scores[month] = {
          "score": score,
          "best_inputs": best_inputs
        }
        print('ZONE:', zone_name, 'MONTH:', month, 'SCORE:', score, 'INPUTS:', best_inputs)

        # print score value
        # score = round(xgb_score, 4)
        # scores[month] = score
        # score_text = '{}:{}: {}'.format(zone_name, month, score)
        # print(score_text)
        continue
    
    for attr, value in month_scores.items():
        print(attr, value)

    with open(save_directory + '/' + zone_name + '/' + 'monthly_model_scores.json', "w") as outfile:
        json.dump(month_scores, outfile)