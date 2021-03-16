import json
import pandas as pd
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import mean_squared_error as MSE, r2_score
import math
import time
from xgboost import plot_importance

all_zones_df = pd.read_csv("../data/scsb_all_zones.csv")
zone_25_df = pd.read_csv("../data/scsb_zone_25.csv")
zone_26_df = pd.read_csv("../data/scsb_zone_26.csv")
zone_27_df = pd.read_csv("../data/scsb_zone_27.csv")

month_dependant_variables = ['jan_dist','feb_dist','mar_dist','apr_dist','may_dist','jun_dist','jul_dist','aug_dist','sep_dist','oct_dist','nov_dist','dec_dist']

data = zone_25_df
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

X = X.tail(30)
y = y.tail(30)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=42)

# One Time Split
xgb = XGBRegressor(random_state=42)
xgb.fit(X_train, y_train)
xgb_pred = xgb.predict(X_test)
print('Score XGBoost Regressor', xgb.score(X_test, y_test))
plot_importance(xgb, title='One Time Split')

# plt.bar(range(len(xgb.feature_importances_)), xgb.feature_importances_)
# plt.show()

# KFold Validation
folds = 10
best_model = {}
max_r2, min_r2, acc_r2 = 0, math.inf, []
kfold = KFold(n_splits=folds, shuffle=True, random_state=42)
for train_index, test_index in kfold.split(X, y):
    # print("--- %s seconds ---" % (time.time() - start_time))
    print("TRAIN:", train_index, "TEST:", test_index)

    X_train , X_test = X.iloc[train_index,:],X.iloc[test_index,:]
    y_train , y_test = y[train_index] , y[test_index]

    model = XGBRegressor(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    score = model.score(X_test, y_test)
    acc_r2.append(score)
    if score > max_r2:
        max_r2 = score
        best_model = model
    if score < min_r2:
        min_r2 = score

avg_r2_score = sum(acc_r2)/folds
print('r2 of each fold - {}'.format(acc_r2))
print('R2 values:')
print("min:", min_r2)
print('avg: {}'.format(avg_r2_score))
print("max:", max_r2) 
print("Feature Importances:", best_model.feature_importances_)
plot_importance(best_model, title='KFold Validation')
# plt.bar(range(len(best_model.feature_importances_)), best_model.feature_importances_)
plt.show()