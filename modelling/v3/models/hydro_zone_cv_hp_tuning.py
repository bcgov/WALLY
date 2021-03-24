import os
import json
import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GridSearchCV
import math
from ast import literal_eval
from time import sleep

directory = '../data/training_data_hydro_zone_annual_flow/nov23/'
dependant_variable = 'mean'
scores = {}

inputs = ["year","drainage_area","average_slope","glacial_coverage","glacial_area","watershed_area","potential_evapotranspiration_thornthwaite","potential_evapotranspiration_hamon","annual_precipitation","median_elevation","aspect","solar_exposure"]
columns = list(inputs) + [dependant_variable]

params = {
  'nthread':[6], #when use hyperthread, xgboost may become slower
  'objective':['reg:squarederror'],
  'learning_rate': [.03, 0.05, .07], #so called `eta` value
  'max_depth': [5, 6, 7],
  'min_child_weight': [4, 5, 6],
  # 'subsample': [0.7, 0.85, 0.95],
  'subsample': [0.7],
  # 'colsample_bytree': [0.7, 0.85, 0.95],
  'colsample_bytree': [0.7],
  'n_estimators': [500]
}

xgb = XGBRegressor()
folds = 5
grid = GridSearchCV(estimator=xgb, param_grid=params, n_jobs=6, cv=folds, verbose=1)

for filename in sorted(os.listdir(directory)):
    if filename.endswith(".csv"):
        zone_name = filename.split('_')[1].split('.')[0]
        print("Starting CV for Zone:", zone_name)

        zone_df = pd.read_csv(os.path.join(directory, filename))

        features_df = zone_df[columns]
        # print(features_df.head())
        # print(features_df.columns)

        X = features_df.dropna(subset=columns) # drop NaNs
        if X.size <=0:
            continue

        Y = X.get(dependant_variable) # dependant
        # print(Y)
        X = X.drop([dependant_variable], axis=1) # independant
        # print(X)

        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.20, random_state=42)
        
        print('Fitting zone:', zone_name)
        grid.fit(X, Y)

        # print('\n All results:')
        # print(grid.cv_results_)
        # print('\n Best estimator:')
        # print(grid.best_estimator_)
        print('\n Best score:')
        print(grid.best_score_ * 2 - 1)
        print('\n Best parameters:')
        print(grid.best_params_)
        print()

        score = grid.best_estimator_.score(X_test, y_test)
        print("r2:", score)

        results = {
          'cv_score': grid.best_score_,
          'r2': score,
          'params': grid.best_params_
        }

        with open('./results/hz-{}-grid-search-results.json'.format(zone_name), "w") as outfile:
            json.dump(results, outfile)
