#!/usr/bin/env python3

import os
import requests as req
import csv 
import time
import datetime
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

tic = time.time()

token = os.getenv("STAGING_TOKEN", "")
# token = os.getenv("PROD_TOKEN", "")

# Add Wally access token here
headers = {'Authorization': 'Bearer ' + token}

# Read in station locations
stations_df = pd.read_csv("../data/bc_mean_annual_flows.csv")

filepath = "../data/watershed_ids.csv"

# Check if we have existing data
try:
    existing_stations_df = pd.read_csv("../data/watershed_ids.csv")
    existing_stations_list = existing_stations_df["station_number"].tolist()
except:
    existing_stations_list = []

watershed_info = []
row_count = 0
already_exists_count = 0
success_count = 0
resp_error_count = 0

def log_progress():
    # if(len(watershed_info) <= 0):
    #     print("no watershed info")

    if row_count % 10 != 0:
        return

    print("*** LOG PROGRESS ***")
    print("row count: {}".format(row_count))

    toc = time.time()
    print("process time: {} minutes".format((toc-tic)/60))

    # data_size = stations_df.size
    failed_call_perc = (resp_error_count / row_count) * 100
    print("already existing stations: {}/{}".format(already_exists_count, len(existing_stations_list)))
    print("failed calls: {} {}%".format(resp_error_count, failed_call_perc))
    print("successful stations count: {} out of {}".format(success_count + already_exists_count, row_count))
    print("successful stations percentage: {}%".format((success_count / row_count) * 100))
    print("*** LOG END ***")


# gets station info from wally and appends to output csv file on each response if data exists
with open(filepath, "a") as outfile:
    writer=csv.writer(outfile)
    for row in stations_df.iterrows():
        row_count += 1
        station = row[1]

        if station["STATION_NUMBER"] in existing_stations_list:
            print("station data already exists")
            already_exists_count += 1
            continue
        
        params = {
          'point': '[{},{}]'.format(station["LONGITUDE"], station["LATITUDE"]),
          'upstream_method': 'DEM'
        }

        resp = req.get("https://wally-staging.apps.silver.devops.gov.bc.ca/api/v1/watersheds/", params=params, headers=headers)
        
        # check for usual bad gateway error and skip
        if resp.status_code != 200:
            # print("error url: {}".format(resp.url))
            resp_error_count += 1
            log_progress()
            continue
        
        try:
            result = resp.json()
        except:
            print(resp.text)
            continue

        if result is None:
            print("result is null")
            continue
        
        watershed = result["watershed"]
        if watershed is None:
            print("watershed is null")
            print(result)
            continue
        
        properties = watershed["properties"]
        if properties is None:
            print("properties is null")
            print(watershed)
            continue
        
        # id,gen_id,processing_time,stream_name,feature_area_sqm,station_number,most_recent_year,mean,min,max,drainage_area_gross,latitude,longitude
        
        info = {
          "id": result["wally_watershed_id"],
          "gen_id": result["generated_watershed_id"],
          "processing_time": result["processing_time"],
          "stream_name": properties["stream_name"],
          "feature_area_sqm": properties["FEATURE_AREA_SQM"],
          "station_number": station["STATION_NUMBER"],
          "most_recent_year": station["YEAR"],
          "mean": station["MEAN"],
          "min": station["MIN"],
          "max": station["MAX"],
          "drainage_area_gross": station["DRAINAGE_AREA_GROSS"],
          "latitude": station["LATITUDE"],
          "longitude": station["LONGITUDE"],
        }
        
        print("station: {}, slope: {}, url: {}".format(info["station_number"], info["id"], resp.url))

        watershed_info.append(info)
        writer.writerow(info.values())

        success_count += 1
        log_progress()

log_progress()