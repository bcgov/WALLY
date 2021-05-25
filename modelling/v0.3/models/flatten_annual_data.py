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

directory = '../data/training_data_hydro_zone_annual_flow/nov23/'
output_dir = "./flattened_data/annual/"

for filename in sorted(os.listdir(directory)):
    if filename.endswith(".csv"):
        zone_name = filename.split('_')[1].split('.')[0]
        
        zone_df = pd.read_csv(os.path.join(directory, filename))
        station_groups = zone_df.groupby("station_number")
        
        latest_independant_vars = station_groups.last().reset_index()
        print("latest_independant_vars")
        print(latest_independant_vars)
        
        yearly_mar_avg = station_groups['mean'].mean().reset_index()
        print("yearly_mar_avg")
        print(yearly_mar_avg)

        latest_independant_vars['mean'] = yearly_mar_avg['mean']
        
        flattened_years = latest_independant_vars
        print("flattened_years")
        print(flattened_years)
        flattened_years.to_csv(output_dir + "zone_" + zone_name + ".csv", index=False)
