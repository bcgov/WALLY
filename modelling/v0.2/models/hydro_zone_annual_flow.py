import os
import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
import math
from ast import literal_eval

directory = '../data/training_data_hydro_zone_annual_flow/'
dependant_variable = 'mean'
scores = []

for filename in sorted(os.listdir(directory)):
    if filename.endswith(".csv"):
        zone_df = pd.read_csv(os.path.join(directory, filename))

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

        # temperature = [] 
        # literal_temps = X.loc[:, "temperature_data"].apply(literal_eval)
        # for temps in literal_temps:
        #     if temps is not None:
        #         temperature.append(sum([monthTemps[2] for monthTemps in temps])/12)

        # X.loc[:, "temperature_data(average field)"] = temperature
        # X = X.drop(['temperature_data'], axis=1)

        y = X.get(dependant_variable) # dependant
        X = X.drop([dependant_variable], axis=1) # independant
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

        xgb = XGBRegressor(random_state=42)
        xgb.fit(X_train, y_train)
        xgb_score = xgb.score(X_test, y_test)

        zone_name = filename.split('_')[1].split('.')[0]
        xgb.save_model('../model_output/hydro_zone_annual_flow/zone_{}.json'.format(zone_name))

        print('{}: {}'.format(zone_name, round(xgb_score, 4)))
        score = '{' + '{}: {}'.format(zone_name, round(xgb_score, 4)) + '}'
        scores.append(score)
        continue
    else:
        continue

# print(scores)
