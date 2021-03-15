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

dtr = DecisionTreeRegressor(random_state=42)
dtr.fit(X_train, y_train)
dtr_pred = dtr.predict(X_test)
print('Score Decision Tree Regressor', dtr.score(X_test, y_test))
print('R2 Decision Tree Regressor', r2_score(y_test, dtr_pred))
# Mean square error Decision Tree Regressor
dtr_mse = MSE(y_test, dtr_pred)
print('Mean Square Error Decision Tree Regressor', dtr_mse)
# Root mean square error Decision Tree Regressor
dtr_rmse = math.sqrt(dtr_mse)
print('Root Mean Square Error Decision Tree Regressor', dtr_rmse)
dtr_output = dtr.predict(X)
print()
# pyplot.bar(range(len(dtr.feature_importances_)), dtr.feature_importances_)
# pyplot.show()

# tree.plot_tree(dtr)

xgb = XGBRegressor(random_state=42)
xgb.fit(X_train, y_train)
xgb_pred = xgb.predict(X_test)
print('Score XGBoost Regressor', xgb.score(X_test, y_test))
# Mean square error XGBoost Regressor
xgb_mse = MSE(y_test, xgb_pred)
print('Mean Square Error XGBoost Regressor', xgb_mse)
# Root mean square error XGBoost Regressor
xgb_rmse = math.sqrt(xgb_mse)
print('Root Mean Square Error XGBoost Regressor', xgb_rmse)
print()
# print(xgb_pred)
xgb_output = xgb.predict(X)

# print('Cross Entropy: {}'.format(log_loss(y_true, y_pred_proba)))
# print('Accuracy: {}'.format(accuracy_score(y_test, xgb_pred)))
# print('Coefficient Kappa: {}'.format(cohen_kappa_score(y_test, xgb_pred)))
print('Classification Report:')
print(xgb.feature_importances_)
print("Confussion Matrix:")
# print(confusion_matrix(y_test, xgb_pred))
# pyplot.bar(range(len(xgb.feature_importances_)), xgb.feature_importances_)
# pyplot.show()
plot_importance(xgb)


rfr = RandomForestRegressor(random_state=42)
rfr.fit(X_train, y_train)
rfr_pred = rfr.predict(X_test)

print('Score Random Forest Regressor', rfr.score(X_test, y_test))
# Mean square error Random Forest Regressor
rfr_mse = MSE(y_test, rfr_pred)
print('Mean Square Error Random Forest Regressor', rfr_mse)
# Root mean square error Random Forest Regressor
rfr_rmse = math.sqrt(rfr_mse)
print('Root Mean Square Error Random Forest Regressor', rfr_rmse)
print()
# print(rfr_pred)
rfr_output = rfr.predict(X)
pyplot.bar(range(len(rfr.feature_importances_)), rfr.feature_importances_)
pyplot.show()

# Output comparisons
output_df = pd.DataFrame()
output_df[['id', 'name']] = data[['id', 'name']]
output_df['SCSB'] = y
output_df['SK_LINEAR'] = lin_output
output_df['SK_RANDOMFOREST'] = rfr_output
output_df['SK_DECISIONTREE'] = dtr_output
output_df['XGBOOST'] = xgb_output

output_df = output_df.round(2)
output_df = output_df.set_index('id')
output_df.to_csv('zone26-models-comparison.csv')

data = data.drop_duplicates(subset=['name'])

# plt.clf()
start = 16
end = 30
data = data.iloc[start:end]

plt.plot(data['name'], y.iloc[start:end], 'go', label='SCSB', color='blue', alpha=0.5)
plt.plot(data['name'], lin_output[start:end], 'go', label='SK_LINEAR', color='purple', alpha=0.5)
plt.plot(data['name'], rfr_output[start:end], 'go', label='SK_RANDOMFOREST', color='red', alpha=0.5)
plt.plot(data['name'], dtr_output[start:end], 'go', label='SK_DECISIONTREE', color='green', alpha=0.5)
plt.plot(data['name'], xgb_output[start:end], 'go', label='XGBOOST', color='black', alpha=0.5)
plt.legend(loc='best')
# plt.xticks(data['name'],"")
plt.xlabel('GNIS Name')
plt.ylabel('MAR')
plt.show()



