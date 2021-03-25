import os
import json
import pandas as pd
from xgboost import XGBRegressor, plot_importance
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from matplotlib import pyplot
import math
import itertools
from ast import literal_eval
from sklearn.model_selection import GridSearchCV, KFold

directory = '../data/training_data_hydro_zone_annual_flow/nov23/'
dependant_variable = 'mean'
zone_scores = {}
count = 0

# inputs = ["year","drainage_area","watershed_area","aspect","solar_exposure","potential_evapotranspiration_hamon",]
inputs = ["average_slope","glacial_coverage","glacial_area","potential_evapotranspiration_thornthwaite","annual_precipitation","median_elevation"]
columns = list(inputs) + [dependant_variable]

show_error_plots = False

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
  'n_estimators': [300]
}

model = XGBRegressor(random_state=42)
folds = 15
# grid = GridSearchCV(estimator=model, param_grid=params, n_jobs=6, cv=folds, verbose=1, scoring='neg_root_mean_squared_error')
kf = KFold(n_splits=folds, random_state=None, shuffle=True)

for filename in sorted(os.listdir(directory)):
    if filename.endswith(".csv"):
        best_r_squared = 0
        best_inputs = []
        # model = XGBRegressor(random_state=42)
        zone_name = filename.split('_')[1].split('.')[0]
        zone_df = pd.read_csv(os.path.join(directory, filename))
        
        df_inputs =  list(inputs) + [dependant_variable]
        print(df_inputs)
        features_df = zone_df[df_inputs]
        X = features_df.dropna(subset=df_inputs) # drop NaNs

        y = X[dependant_variable] # dependant
        X = X.drop([dependant_variable], axis=1) # independant
        mean_mar = round(y.mean(),4)

        if len(X.index) <=1:
            continue

        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

        best_model = None
        for train_index, test_index in kf.split(X):
            X_train, X_test = X.iloc[train_index,:], X.iloc[test_index,:]
            y_train, y_test = y.iloc[train_index].values.ravel(), y.iloc[test_index].values.ravel()

            eval_set = [(X_train, y_train), (X_test, y_test)]

            # grid.fit(X_train, y_train, eval_set=eval_set, eval_metric=["rmse", "logloss"], early_stopping_rounds=10)
            model.fit(X_train, y_train, eval_set=eval_set, eval_metric=["rmse", "logloss"], early_stopping_rounds=10)

            # TODO
            # minimum number of years
            # track highest rmse, highest R2/lowest RMSE
            # choose model with highest minimum r2
            # look at furthest outlier, compare the two versions
            # build comparison graph, 

            y_pred = model.predict(X_test)
            r2 = r2_score(y_test, y_pred) # model.score(X_test, y_test)
            rmse = mean_squared_error(y_test, y_pred, squared=False)
            results = model.evals_result()
            
            model_test = { 
                "model": model,
                "mean_mar": mean_mar,
                "r2": round(r2,4),
                "rmse": round(rmse,6),
                "results": results
            }

            if best_model is None:
                best_model = model_test
            elif rmse < best_model['rmse']:
                best_model = model_test


        model = best_model['model']
        results = best_model['results']
        rmse = best_model['rmse']
        r2 = best_model['r2']
        mean_mar = best_model['mean_mar']
        
        # results = grid.cv_results_
        # print(results)
        print("zone", zone_name)
        print("r2 score", r2)
        rmse = results["validation_1"]["rmse"][-1]
        rmse_95_p = rmse * 2
        print("RMSE 95%", rmse_95_p)

        if show_error_plots:
            epochs = len(results["validation_0"]["rmse"])
            x_axis = range(0, epochs)
            # plot rmse loss
            fig, ax = pyplot.subplots(figsize=(12,12))
            ax.plot(x_axis, results["validation_0"]["rmse"], label="Train")
            ax.plot(x_axis, results["validation_1"]["rmse"], label="Test")
            ax.legend()
            pyplot.ylabel("RMSE")
            pyplot.title("XGBoost RMSE")
            # plot log error
            # fig, ax = pyplot.subplots(figsize=(12,12))
            # ax.plot(x_axis, results["validation_0"]["logloss"], label="Train")
            # ax.plot(x_axis, results["validation_1"]["logloss"], label="Test")
            # ax.legend()
            # pyplot.ylabel("Log Error")
            # pyplot.title("XGBoost Log Error")

            plot_importance(model)
            pyplot.show()

        # raw_uncertainty = rmse / mean_mar
        # uncertainty = round(rmse / mean_mar, 4) * 100
        zone_name = filename.split('_')[1].split('.')[0]
        model.save_model('../model_output/hydro_zone_annual_flow/zone_{}.json'.format(zone_name))

        zone_scores[zone_name] = {
          "R2": r2,
          "RMSE_68%": rmse,
          "RMSE_95%": rmse_95_p,
          # "MAR": mean_mar,
          # "+/-": str(uncertainty) + '%',
          # "raw": raw_uncertainty
        }

    else:
        continue

print()
print("Zone Model Results")
r2_sum = 0
rmse_sum = 0
rmse_95_sum = 0
for attr, value in zone_scores.items():
    print(attr, value)
    if not math.isnan(value["R2"]):
        r2_sum += value["R2"]
    if value["RMSE_68%"]:
        rmse_sum += value["RMSE_68%"]
    if value["RMSE_95%"]:
        rmse_95_sum += value["RMSE_95%"]

print("Score Totals for BC")
# print("R2", r2_sum)
print("RMSE_68%_Sum", rmse_sum)
print("RMSE_95%_Sum", rmse_95_sum)


with open('../model_output/hydro_zone_annual_flow/annual_model_scores.json', "w") as outfile:
    json.dump(zone_scores, outfile)
