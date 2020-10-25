import os
import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
import math

parent_directory = '../data/hydro_zone_monthly_distributions'
dependant_variable = 'MONTHLY_MEAN'

for zone in range(1, 29): # zones
    zone_name = 'zone_' + str(zone)
    for month in range(1, 12): # months
        month_name = 'month_' + month

        file_path = parent_directory + '/' + zone_name + '/' + month_name + '.csv'
        zone_df = pd.read_csv(file_path)

        # feature engineering
        # drop data from years above 2017
        # indexNames = zone_df[ zone_df['YEAR'] > 2017 ].index
        # zone_df.drop(indexNames, inplace=True)

        columns = ['drainage_area', 'median_elevation', 'annual_precipitation', dependant_variable]

        features_df = zone_df[columns]
        X = features_df.dropna(subset=columns) # drop NaNs
        X = X.drop([dependant_variable], axis=1) # independant
        y = features_df.get(dependant_variable) # dependant
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

        xgb = XGBRegressor(random_state=42)
        xgb.fit(X_train, y_train)
        xgb_score = xgb.score(X_test, y_test)

        # save model output state
        save_directory = '../model_output/hydro_zone_monthly_distributions'
        save_path = save_directory + '/' + zone_name + '/' + month_name + '.json'
        xgb.save_model(save_path)

        print('{' + '{}:{}: {}'.format(zone_name, month_name, round(xgb_score, 4)) + '}')
        continue
