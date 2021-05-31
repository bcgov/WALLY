import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error as MSE, r2_score
import math

with open('../../data/output/training_data/annual_mean_training_dataset_08-11-2020.json', 'r') as f:
    data = json.load(f)

filtered_data = [item for item in data 
  if item["median_elevation"] != None and
  item["MEAN"] < 100 and
  item["annual_precipitation"] < 6000 and 
  item["drainage_area"] < 200
]

df = pd.DataFrame(filtered_data)
df.head()

temperature = [] 
for temps in df["temperature_data"]:
    temperature.append(sum([monthTemps[2] for monthTemps in temps])/12)

df["temperature_data(average field)"] = temperature
df.head()

features_df = df[['annual_precipitation', 'drainage_area', 'median_elevation', 'average_slope', 'temperature_data(average field)', 'MEAN']]
features_df.head()

X = features_df.drop(['MEAN'], axis=1)
y = features_df.MEAN

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

dtr = DecisionTreeRegressor(random_state=42)
dtr.fit(X_train, y_train)

dtr_pred = dtr.predict(X_test)

print('Score Decision Tree Regressor', dtr.score(X_test, y_test))
# print('R2 Decision Tree Regressor', r2_score(y_test, dtr_pred))

# Mean square error Decision Tree Regressor
dtr_mse = MSE(y_test, dtr_pred)
print('Mean Suqare Error Decision Tree Regressor', dtr_mse)

# Root mean square error Decision Tree Regressor
dtr_rmse = math.sqrt(dtr_mse)
print('Root Mean Suqare Error Decision Tree Regressor', dtr_rmse)


xgb = XGBRegressor(random_state=42)
xgb.fit(X_train, y_train)

xgb_pred = xgb.predict(X_test)

print('Score XGBoost Regressor', xgb.score(X_test, y_test))

# Mean square error XGBoost Regressor
xgb_mse = MSE(y_test, xgb_pred)
print('Mean Suqare Error XGBoost Regressor', xgb_mse)

# Root mean square error XGBoost Regressor
xgb_rmse = math.sqrt(xgb_mse)
print('Root Mean Suqare Error XGBoost Regressor', xgb_rmse)


rfr = RandomForestRegressor(random_state=42)
rfr.fit(X_train, y_train)

rfr_pred = rfr.predict(X_test)

print('Score Decision Tree Regressor', rfr.score(X_test, y_test))

# Mean square error Random Forest Regressor
rfr_mse = MSE(y_test, rfr_pred)
print('Mean Suqare Error Random Forest Regressor', rfr_mse)

# Root mean square error Random Forest Regressor
rfr_rmse = math.sqrt(rfr_mse)
print('Root Mean Suqare Error Random Forest Regressor', rfr_rmse)


# cat = CatBoostRegressor(random_state=42)
# cat.fit(X_train, y_train)

# cat_pred = cat.predict(X_test)

# print('Score CatBoost Regressor', cat.score(X_test, y_test))

# # Mean square error CatBoost Regressor
# cat_mse = MSE(y_test, cat_pred)
# print('Mean Suqare Error CatBoost Regressor', cat_mse)

# # Root mean square error CatBoost Regressor
# cat_rmse = math.sqrt(cat_mse)
# print('Root Mean Suqare Error CatBoost Regressor', cat_rmse)