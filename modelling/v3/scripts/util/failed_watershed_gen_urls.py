import os
import requests as req
import csv 
import json
import time
import datetime
import pandas as pd

directory = '../data/mean_annual_flows/'

# data = pd.read_csv(os.path.join(directory, 'flattened_bc_mean_annual_flows.csv'))

watershed_characteristics = []
resp_error_count = 0
slope_null_count = 0

stations_df = pd.read_csv("../data/watershed_ids.csv")
existing_stations_df = pd.read_csv("../data/watershed_stats.csv")
existing_stations_list = existing_stations_df["station_number"].tolist()


for index, station in stations_df.iterrows():
    if station["STATION_NUMBER"] not in existing_stations_list:
        print(
          "https://wally-staging.apps.silver.devops.gov.bc.ca/api/v1/watersheds/?point=%5B{}%2C{}%5D&include_self=false&upstream_method=DEM".format(station["LONGITUDE"], station["LATITUDE"])
        )