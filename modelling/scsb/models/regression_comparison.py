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

# with open('../../data/output/training_data/annual_mean_training_dataset_08-11-2020.json', 'r') as f:
#     data = json.load(f)

all_zones_df = pd.read_csv("../data/scsb_all_zones.csv")
zone_25_df = pd.read_csv("../data/scsb_zone_25.csv")
zone_26_df = pd.read_csv("../data/scsb_zone_26.csv")
zone_27_df = pd.read_csv("../data/scsb_zone_27.csv")

month_dependant_variables = ['jan_dist','feb_dist','mar_dist','apr_dist','may_dist','jun_dist','jul_dist','aug_dist','sep_dist','oct_dist','nov_dist','dec_dist']

data = zone_26_df
dependant_variable = 'may_dist'

# features_df = data[['annual_precipitation', 'drainage_area', 'median_elevation', \
#   'average_slope', 'glacial_coverage', 'potential_evapo_transpiration', dependant_variable]]

# zone 25 independant variables
# features_df = data[['annual_precipitation', 'glacial_coverage', 'potential_evapo_transpiration', dependant_variable]]

# zone 26 independant variables
features_df = data[['median_elevation', 'glacial_coverage', 'annual_precipitation', 'potential_evapo_transpiration', dependant_variable]]

# zone 27 independant variables
# features_df = data[['median_elevation', 'annual_precipitation', 'drainage_area', dependant_variable]]


X = features_df.drop([dependant_variable], axis=1)
y = features_df.get(dependant_variable)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)


lin = LinearRegression()
lin.fit(X_train, y_train)
lin_pred = lin.predict(X_test)
print('Score Linear Regressor', lin.score(X_test, y_test))


dtr = DecisionTreeRegressor(random_state=42)
dtr.fit(X_train, y_train)
dtr_pred = dtr.predict(X_test)
print('Score Decision Tree Regressor', dtr.score(X_test, y_test))
# print('R2 Decision Tree Regressor', r2_score(y_test, dtr_pred))
# # Mean square error Decision Tree Regressor
# dtr_mse = MSE(y_test, dtr_pred)
# print('Mean Suqare Error Decision Tree Regressor', dtr_mse)
# # Root mean square error Decision Tree Regressor
# dtr_rmse = math.sqrt(dtr_mse)
# print('Root Mean Suqare Error Decision Tree Regressor', dtr_rmse)


xgb = XGBRegressor(random_state=42)
xgb.fit(X_train, y_train)
xgb_pred = xgb.predict(X_test)
print('Score XGBoost Regressor', xgb.score(X_test, y_test))
# Mean square error XGBoost Regressor
# xgb_mse = MSE(y_test, xgb_pred)
# print('Mean Suqare Error XGBoost Regressor', xgb_mse)
# Root mean square error XGBoost Regressor
# xgb_rmse = math.sqrt(xgb_mse)
# print('Root Mean Suqare Error XGBoost Regressor', xgb_rmse)


rfr = RandomForestRegressor(random_state=42)
rfr.fit(X_train, y_train)
rfr_pred = rfr.predict(X_test)
print('Score Random Forest Regressor', rfr.score(X_test, y_test))
# # Mean square error Random Forest Regressor
# rfr_mse = MSE(y_test, rfr_pred)
# print('Mean Suqare Error Random Forest Regressor', rfr_mse)
# # Root mean square error Random Forest Regressor
# rfr_rmse = math.sqrt(rfr_mse)
# print('Root Mean Suqare Error Random Forest Regressor', rfr_rmse)
