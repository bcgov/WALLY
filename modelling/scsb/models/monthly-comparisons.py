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
month_labels = [x[0:3] for x in month_dependant_variables]

data = zone_26_df

xgb_results = []
rfr_results = []
dtr_results = []

# calculate monthly estimations for 3 models
for dependant_month in month_dependant_variables:
    features_df = data[['median_elevation', 'glacial_coverage', 'annual_precipitation', 'potential_evapo_transpiration', dependant_month]]
    X = features_df.drop([dependant_month], axis=1)
    y = features_df.get(dependant_month)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)
    
    xgb = XGBRegressor(random_state=42)
    xgb.fit(X_train, y_train)
    xgb_results.append(xgb.predict(X))

    rfr = RandomForestRegressor(random_state=42)
    rfr.fit(X_train, y_train)
    rfr_results.append(rfr.predict(X))

    dtr = DecisionTreeRegressor(random_state=42)
    dtr.fit(X_train, y_train)
    dtr_results.append(dtr.predict(X))

# compare the outputs of scsb against the 3 models
for row_target_index in range(20):
    xgb_row = []
    rfr_row = []
    dtr_row = []

    for month in range(12):
        xgb_row.append(xgb_results[month][row_target_index])
        rfr_row.append(rfr_results[month][row_target_index])
        dtr_row.append(dtr_results[month][row_target_index])

    plt.plot(data[month_dependant_variables].iloc[row_target_index], '-', label='scsb', color='blue', alpha=0.5)
    plt.plot(xgb_row, '-', label='xgboost', color='red', alpha=0.5)
    plt.plot(rfr_row, '-', label='randomforest', color='green', alpha=0.5)
    plt.plot(dtr_row, '-', label='decisiontree', color='purple', alpha=0.5)
    plt.legend(loc='best')
    plt.xticks(month_dependant_variables, month_labels)
    plt.xlabel('Month')
    plt.ylabel('Monthly Distribution')
    name = data['name'].iloc[row_target_index]
    plt.title(name)
    plt.savefig('../plots/{}.png'.format(name))
    plt.show()
