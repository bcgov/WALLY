import os
import json
import pandas as pd
import numpy as np
from xgboost import XGBRegressor, plot_importance
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from matplotlib import pyplot
import math
import itertools
from ast import literal_eval
from sklearn.model_selection import GridSearchCV, KFold
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import matplotlib.backends.backend_pdf

# directory = '../data/training_data_hydro_zone_annual_flow/nov23/'
directory = './flattened_data/annual/'
dependant_variable = 'mean'
zone_scores = {}
count = 0

# inputs = ["year","drainage_area","watershed_area","aspect","glacial_area","solar_exposure","potential_evapotranspiration_hamon",]
inputs = ["average_slope","glacial_coverage","potential_evapotranspiration_thornthwaite","annual_precipitation","median_elevation","aspect","solar_exposure"]
columns = list(inputs) + [dependant_variable]

for filename in sorted(os.listdir(directory)):
    if filename.endswith(".csv"):
        best_r_squared = 0
        best_inputs = []
        # model = XGBRegressor(random_state=42)
        zone_name = filename.split('_')[1].split('.')[0]
        output_dir = "./outputs/annual_flow_regressions/"
        zone_df = pd.read_csv(os.path.join(directory, filename))
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        pdf = matplotlib.backends.backend_pdf.PdfPages(output_dir + "zone_" + str(zone_name) + ".pdf")
            
        df_inputs =  list(inputs) + [dependant_variable]
        print(df_inputs)
        features_df = zone_df[df_inputs]

        X = features_df.dropna(subset=df_inputs) # drop NaNs
        # X = features_df
        y = X[dependant_variable] # dependant
        X = X.drop([dependant_variable], axis=1) # independant

        print(y)
        print(X)

        size = (8, 6)
        marker_size = 9
        for feature in inputs:
            fig_test, axt = plt.subplots(figsize=size)
            axt = sns.regplot(X[feature], y, fit_reg=True) 
            # xlim = axt.get_xlim()[1]
            # ylim = axt.get_ylim()[1]
            # max_size = max(xlim, ylim)
            axt.set_xlabel(feature)
            axt.set_ylabel('mean')
            # lx = np.linspace(0,max_size/2,100)
            # lx = np.linspace(0,50,100)
            # ly = lx
            # axt.plot(lx, ly, ':')
            # axt.legend()
            pdf.savefig( fig_test )
        
        pdf.close()
        