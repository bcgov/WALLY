import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error as MSE, r2_score
import math

directory = '../../data/output/hydrological_zones'
dependant_variable = 'MEAN'

for filename in sorted(os.listdir(directory)):
    if filename.endswith(".csv"):
        zone_df = pd.read_csv(os.path.join(directory, filename))

        indexNames = zone_df[ zone_df['YEAR'] > 2017 ].index
        zone_df.drop(indexNames, inplace=True)

        features_df = zone_df[['drainage_area', 'median_elevation', 'annual_precipitation', dependant_variable]]
        X = features_df.drop([dependant_variable], axis=1)
        
        # print(X.isna().sum())
        # remove NaNs
        X = pd.DataFrame(X).fillna(0)

        y = features_df.get(dependant_variable)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)
        
        dtr = DecisionTreeRegressor(random_state=42)
        dtr.fit(X_train, y_train)
        dtr_score = dtr.score(X_test, y_test)

        rfr = RandomForestRegressor(random_state=42)
        rfr.fit(X_train, y_train)
        rft_score = rfr.score(X_test, y_test)

        xgb = XGBRegressor(random_state=42)
        xgb.fit(X_train, y_train)
        xgb_score = xgb.score(X_test, y_test)

        max_score = max(dtr_score, rft_score, xgb_score)
        zone_name = filename.split('_')[1].split('.')[0]

        # rfr.save_model('./model_io/rfr/zone_{}.json'.format(zone_name))
        xgb.save_model('./model_io/xgb/zone_{}.json'.format(zone_name))

        # print('zone {}: r2: {} stn_count: {}'.format(zone_name, round(max_score, 3), len(X)))
        print('{}'.format(round(max_score, 6)))
        continue
    else:
        continue


# lin = LinearRegression()
# lin.fit(X_train, y_train)
# lin_pred = lin.predict(X_test)
# print('Score Linear Regressor', lin.score(X_test, y_test))


# dtr = DecisionTreeRegressor(random_state=42)
# dtr.fit(X_train, y_train)
# dtr_pred = dtr.predict(X_test)
# print('Score Decision Tree Regressor', dtr.score(X_test, y_test))

# print('R2 Decision Tree Regressor', r2_score(y_test, dtr_pred))
# # Mean square error Decision Tree Regressor
# dtr_mse = MSE(y_test, dtr_pred)
# print('Mean Suqare Error Decision Tree Regressor', dtr_mse)
# # Root mean square error Decision Tree Regressor
# dtr_rmse = math.sqrt(dtr_mse)
# print('Root Mean Suqare Error Decision Tree Regressor', dtr_rmse)


# xgb = XGBRegressor(random_state=42)
# xgb.fit(X_train, y_train)
# xgb_pred = xgb.predict(X_test)
# print('Score XGBoost Regressor', xgb.score(X_test, y_test))

# Mean square error XGBoost Regressor
# xgb_mse = MSE(y_test, xgb_pred)
# print('Mean Suqare Error XGBoost Regressor', xgb_mse)
# Root mean square error XGBoost Regressor
# xgb_rmse = math.sqrt(xgb_mse)
# print('Root Mean Suqare Error XGBoost Regressor', xgb_rmse)


# rfr = RandomForestRegressor(random_state=42)
# rfr.fit(X_train, y_train)
# rfr_pred = rfr.predict(X_test)
# print('Score Random Forest Regressor', rfr.score(X_test, y_test))

# # Mean square error Random Forest Regressor
# rfr_mse = MSE(y_test, rfr_pred)
# print('Mean Suqare Error Random Forest Regressor', rfr_mse)
# # Root mean square error Random Forest Regressor
# rfr_rmse = math.sqrt(rfr_mse)
# print('Root Mean Suqare Error Random Forest Regressor', rfr_rmse)

