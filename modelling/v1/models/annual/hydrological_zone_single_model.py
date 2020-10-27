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

file_path = '../../data/output/hydrological_zones/zone_26.csv'
dependant_variable = 'MEAN'

zone_df = pd.read_csv(file_path)

indexNames = zone_df[ zone_df['YEAR'] > 2017 ].index
zone_df.drop(indexNames, inplace=True)

features_df = zone_df[['drainage_area', 'median_elevation', 'glacial_coverage', 'annual_precipitation', dependant_variable]]
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
# zone_name = filename.split('_')[1].split('.')[0]

# rfr.save_model('./model_io/rfr/zone_{}.json'.format(zone_name))
# xgb.save_model('./model_io/xgb/{}.json'.format(file_path.split('/')[-1].split('.')[0]))

print('{}: r2: {} row_count: {}'.format(file_path.split('/')[-1], round(max_score, 3), len(X)))
# print('{}'.format(round(max_score, 6)))
# print('{' + '{}: {}'.format(zone_name, round(max_score, 4)) + '}')