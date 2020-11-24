import os
import json
import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
import math

parent_directory = '../data/training_data_hydro_zone_monthly_distributions'
dependant_variable = 'monthly_mean'

inputs_list = ["year","drainage_area","drainage_area_gross","average_slope","glacial_coverage","glacial_area","watershed_area","potential_evapotranspiration_thornthwaite","potential_evapotranspiration_hamon","hydrological_zone","annual_precipitation","median_elevation","aspect","solar_exposure"]
# inputs_list = ["drainage_area", "average_slope", "glacial_coverage", "glacial_area", "annual_precipitation", "median_elevation", "potential_evapotranspiration_thornthwaite", "aspect", "solar_exposure"]
# inputs_list = ["drainage_area", "glacial_coverage", "glacial_area", "annual_precipitation", "potential_evapotranspiration_thornthwaite"]

for zone in range(1, 30): # zones
    zone_name = 'zone_' + str(zone)
    scores = {}
    for month in range(1, 13): # months
        file_path = parent_directory + '/' + zone_name + '/' + str(month) + '.csv'
        zone_df = pd.read_csv(file_path)

        # feature engineering
        # drop data from years above 2017
        # indexNames = zone_df[ zone_df['YEAR'] > 2017 ].index
        # zone_df.drop(indexNames, inplace=True)

        columns = ['drainage_area', 'annual_precipitation', 
          'glacial_coverage', 'glacial_area', dependant_variable]

        features_df = zone_df[columns]
        X = features_df.dropna(subset=columns) # drop NaNs
        if X.size <=0:
            continue

        X = X.drop([dependant_variable], axis=1) # independant
        y = features_df.get(dependant_variable) # dependant
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

        xgb = XGBRegressor(random_state=42)
        xgb.fit(X_train, y_train)
        xgb_score = xgb.score(X_test, y_test)

        # save model output state
        month = str(month)
        save_directory = '../model_output/hydro_zone_monthly_distributions'
        save_path = save_directory + '/' + zone_name + '/' + month + '.json'
        xgb.save_model(save_path)

        # print score value
        score = round(xgb_score, 4)
        scores[month] = score
        score_text = '{}:{}: {}'.format(zone_name, month, score)
        print(score_text)
        continue

    with open(save_directory + '/' + zone_name + '/' + 'monthly_model_scores.json', "w") as outfile:
        json.dump(scores, outfile)