import os
import json
import pandas as pd
from matplotlib import pyplot
import math
import itertools
from ast import literal_eval
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import matplotlib.backends.backend_pdf

directory = '../data/training_data_hydro_zone_monthly_distributions/nov23/'
output_dir = "./flattened_data/monthly/"

for zone in range(1, 30): # zones
    zone_name = 'zone_' + str(zone)
    scores = {}
    for month in range(1, 13): # months
        file_path = directory + '/' + zone_name + '/' + str(month) + '.csv'
        zone_df = pd.read_csv(file_path)

        station_groups = zone_df.groupby("station_number")
        
        latest_independant_vars = station_groups.last().reset_index()
        print("latest_independant_vars")
        print(latest_independant_vars)
        
        averages = station_groups[['monthly_mean','monthly_total','min','max']].mean().reset_index()
        latest_independant_vars[['monthly_mean','monthly_total','min','max']] = averages[['monthly_mean','monthly_total','min','max']]
        
        flattened_years = latest_independant_vars
        print("flattened_years")
        print(flattened_years)

        save_dir = output_dir + zone_name + '/'
        filename = str(month) + '.csv'
        if not os.path.exists(save_dir):  
            os.mkdir(save_dir)
        save_path = os.path.join(save_dir, filename)

        flattened_years.to_csv(save_path, index=False)
