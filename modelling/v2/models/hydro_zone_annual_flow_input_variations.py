import os
import json
import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
import math
import itertools
from ast import literal_eval

directory = '../data/training_data_hydro_zone_annual_flow/nov16/'
dependant_variable = 'mean'
zone_scores = {}
count = 0

# inputs_list = ["year","drainage_area","drainage_area_gross","average_slope","glacial_coverage","glacial_area","watershed_area","potential_evapotranspiration_thornthwaite","potential_evapotranspiration_hamon","hydrological_zone","annual_precipitation","median_elevation","aspect","solar_exposure"]
inputs_list = ["drainage_area_gross", "drainage_area", "watershed_area", "average_slope", "glacial_coverage", "glacial_area", "annual_precipitation", "median_elevation", "potential_evapotranspiration_thornthwaite", "aspect", "solar_exposure"]

all_combinations = []
for r in range(len(inputs_list) + 1):
    combinations_object = itertools.combinations(inputs_list, r)
    combinations_list = list(combinations_object)
    all_combinations += combinations_list

# limit input list size
all_combinations = [x for x in all_combinations if len(x)<=4]

print('total combinations: ', len(all_combinations))

for filename in sorted(os.listdir(directory)):
    if filename.endswith(".csv"):
        best_r_squared = 0
        best_inputs = []
        xgb = XGBRegressor(random_state=42)
        zone_name = filename.split('_')[1].split('.')[0]
        zone_df = pd.read_csv(os.path.join(directory, filename))

        for inputs in all_combinations:
            count += 1
            # year = 2015

            # feature engineering
            # drop data from years above 2017
            # indexNames = zone_df[ zone_df['year'] > 2015 ].index
            # zone_df.drop(indexNames, inplace=True)

            # inputs = ['drainage_area', 'annual_precipitation', 
            #   'glacial_coverage', 'glacial_area', dependant_variable]
            
            inputs = list(inputs) + [dependant_variable]
            if len(inputs) < 2:
                continue

            features_df = zone_df[inputs]
            X = features_df.dropna(subset=inputs) # drop NaNs


            # temperature = [] 
            # literal_temps = X.loc[:, "temperature_data"].apply(literal_eval)
            # for temps in literal_temps:
            #     if temps is not None:
            #         temperature.append(sum([monthTemps[2] for monthTemps in temps])/12)

            # X.loc[:, "temperature_data(average field)"] = temperature
            # X = X.drop(['temperature_data'], axis=1)

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
                xgb.save_model('../model_output/hydro_zone_annual_flow_nov16/zone_{}.json'.format(zone_name))
            
            # print(count, xgb_score, X.columns.values)
            # print(count)

        # print score value
        score = round(best_r_squared, 5)
        zone_scores[zone_name] = {
          "score": score,
          "best_inputs": best_inputs
        }
        print('ZONE:', zone_name, 'SCORE:', score, 'INPUTS:', best_inputs)
    else:
        continue
# print(zone_scores)

# create r2 scores
with open('../model_output/hydro_zone_annual_flow_nov16/annual_model_scores.json', "w") as outfile:
    json.dump(zone_scores, outfile)