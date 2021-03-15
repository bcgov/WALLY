import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold, KFold
from sklearn.metrics import mean_squared_error as MSE, r2_score
from sklearn.metrics import log_loss, cohen_kappa_score, accuracy_score, confusion_matrix, hinge_loss, classification_report
import math
import time
from matplotlib import pyplot
from xgboost import plot_importance
from sklearn import tree
# with open('../../data/output/training_data/annual_mean_training_dataset_08-11-2020.json', 'r') as f:
#     data = json.load(f)

all_zones_df = pd.read_csv("../data/scsb_all_zones.csv")
zone_25_df = pd.read_csv("../data/scsb_zone_25.csv")
zone_26_df = pd.read_csv("../data/scsb_zone_26.csv")
zone_27_df = pd.read_csv("../data/scsb_zone_27.csv")

month_dependant_variables = ['jan_dist','feb_dist','mar_dist','apr_dist','may_dist','jun_dist','jul_dist','aug_dist','sep_dist','oct_dist','nov_dist','dec_dist']

data = zone_27_df
dependant_variable = 'mean_annual_runoff'
start_time = time.time()

# features_df = data[['annual_precipitation', 'drainage_area', 'median_elevation', \
#   'average_slope', 'glacial_coverage', 'potential_evapo_transpiration', dependant_variable]]

# zone 25 independant variables
# features_df = data[['annual_precipitation', 'glacial_coverage', 'potential_evapo_transpiration', dependant_variable]]

# zone 26 independant variables
# features_df = data[['median_elevation', 'glacial_coverage', 'annual_precipitation', 'potential_evapo_transpiration', dependant_variable]]

# zone 27 independant variables
# features_df = data[['median_elevation', 'annual_precipitation', 'average_slope', dependant_variable]]
features_df = data[['median_elevation', 'solar_exposure', 'glacial_coverage', 'annual_precipitation', 'potential_evapo_transpiration', 'average_slope', 'drainage_area', dependant_variable]]


X = features_df.drop([dependant_variable], axis=1)
y = features_df.get(dependant_variable)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=42)

lin = LinearRegression()
lin.fit(X_train, y_train)
lin_pred = lin.predict(X_test)
print('Score Linear Regressor', lin.score(X_test, y_test))
lin_output = lin.predict(X)
print()
print(lin.coef_)
print(lin.intercept_)

# TODO Does running k fold, reduce the importance of variables. See if any algorithms drop importance
# average flow compared to normal flow, Look at HYDAT and normalization, 
folds = 10
max_r2, min_r2, acc_r2 = 0, math.inf, []
kfold = KFold(n_splits=folds, shuffle=True, random_state=42)
for train_index, test_index in kfold.split(X, y):
    # print("--- %s seconds ---" % (time.time() - start_time))
    # print("TRAIN:", train_index, "TEST:", test_index)

    X_train , X_test = X.iloc[train_index,:],X.iloc[test_index,:]
    y_train , y_test = y[train_index] , y[test_index]

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    score = model.score(X_test, y_test)
    acc_r2.append(score)
    if score > max_r2:
        max_r2 = score
    if score < min_r2:
        min_r2 = score

avg_r2_score = sum(acc_r2)/folds
print('r2 of each fold - {}'.format(acc_r2))
print('R2 values:')
print("min:", min_r2)
print('avg: {}'.format(avg_r2_score))
print("max:", max_r2) 
