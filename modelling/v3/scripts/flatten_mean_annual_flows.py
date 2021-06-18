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

directory = '../data/1_source/'

for filename in sorted(os.listdir(directory)):
    if filename.endswith(".csv"):
        # zone_name = filename.split('_')[1].split('.')[0]
        
        zone_df = pd.read_csv(os.path.join(directory, 'bc_mean_annual_flows_unflattened_jun17.csv'))
        station_groups = zone_df.groupby("STATION_NUMBER")
        # print(station_groups.size())
        
        latest_independant_vars = station_groups.last().reset_index()
        print("latest_independant_vars")
        print(latest_independant_vars)
        
        yearly_mar_avg = station_groups['MEAN'].mean().reset_index()
        print("yearly_mar_avg")
        print(yearly_mar_avg)

        station_group_sizes = station_groups.size().reset_index()
        print(station_group_sizes)
        latest_independant_vars['YEARS_OF_DATA'] = station_group_sizes.iloc[:,1]
        print("years of data")
        print(latest_independant_vars['YEARS_OF_DATA'])

        latest_independant_vars['MEAN'] = yearly_mar_avg['MEAN']
        flattened_years = latest_independant_vars
        print("flattened_years")
        print(flattened_years)

        ten_year_stations = flattened_years.loc[flattened_years['YEARS_OF_DATA'] > 10]
        twenty_year_stations = flattened_years.loc[flattened_years['YEARS_OF_DATA'] > 20]

        # print("ten year stations:", ten_year_stations.count())
        # print("twenty year stations:", twenty_year_stations.count())

        # ten_year_stations.to_csv(directory + "yearly_stations/bc_mean_annual_flows_10_year_stations.csv", index=False)
        # twenty_year_stations.to_csv(directory + "yearly_stations/bc_mean_annual_flows_20_year_stations.csv", index=False)
        flattened_years.to_csv(directory + "bc_mean_annual_flows_flattened_jun17.csv", index=False)
