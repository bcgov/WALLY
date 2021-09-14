#!/usr/bin/env python3

import os
import requests as req
import csv 
import time
import datetime
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import base64
from shapely.geometry import Point


load_dotenv()

tic = time.time()

token = os.getenv("STAGING_TOKEN", "")
# token = os.getenv("PROD_TOKEN", "")

# Add Wally access token here
headers = {'Authorization': 'Bearer ' + token}

# Read in station locations
watersheds_df = pd.read_csv("../data/bc_mean_annual_flows.csv")

filepath = "../data/watershed_stats_second_step_output.csv"

# Check if we have existing data
try:
    existing_watersheds_df = pd.read_csv("../data/watershed_stats_second_step_output.csv")
    existing_watersheds_list = existing_watersheds_df["station_number"].tolist()
except:
    existing_watersheds_list = []

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

    failed_call_perc = (resp_error_count / row_count) * 100
    print("already existing watersheds: {}/{}".format(already_exists_count, len(existing_watersheds_list)))
    print("failed calls: {} {}%".format(resp_error_count, failed_call_perc))
    print("successful watersheds count: {} out of {}".format(success_count + already_exists_count, row_count))
    print("successful watersheds percentage: {}%".format((success_count / row_count) * 100))
    print("*** LOG END ***")


# gets station info from wally and appends to output csv file on each response if data exists
with open(filepath, "a") as outfile:
    writer=csv.writer(outfile)
    for row in watersheds_df.iterrows():
        row_count += 1
        watershed = row[1]
        # print(watershed)

        if watershed["STATION_NUMBER"] in existing_watersheds_list:
            print("watershed data already exists")
            already_exists_count += 1
            continue
        
        # params = {
        #   'generated_watershed_id': watershed["gen_id"]
        # }
        print(float(watershed["LONGITUDE"]), float(watershed["LATITUDE"]))
        point = Point(float(watershed["LONGITUDE"]), float(watershed["LATITUDE"]))
        watershed_point = base64.urlsafe_b64encode(
            point.wkb).decode('utf-8')
      
        # point = point_text.encode('utf-8')
        # print(point)

        watershed_id = "generated_dem." + watershed_point
        # print(watershed_id)
        resp = req.get("https://wally-staging.apps.silver.devops.gov.bc.ca/api/v1/watersheds/" + watershed_id, headers=headers)
        
        # check for usual bad gateway error and skip
        if resp.status_code != 200:
            print("error url: {}".format(resp.url))
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
        
        # id,gen_id,processing_time,stream_name,feature_area_sqm,station_number,most_recent_year,mean,min,max,drainage_area_gross,latitude,longitude,annual_precipitation,aspect,average_slope,drainage_area,glacial_area,glacial_coverage,hydrological_zone,median_elevation,potential_evapotranspiration_hamon,potential_evapotranspiration_thornthwaite,solar_exposure,watershed_area,temperature_data
        
        # STATION_NUMBER,YEAR,MEAN,MIN,MAX,MIN_MONTH,MAX_MONTH,LATITUDE,LONGITUDE,DRAINAGE_AREA_GROSS
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

          "annual_precipitation": result["annual_precipitation"],
          "aspect": result["aspect"],
          "average_slope": result["average_slope"],
          "drainage_area": result["drainage_area"],
          "glacial_area": result["glacial_area"],
          "glacial_coverage": result["glacial_coverage"],
          "hydrological_zone": result["hydrological_zone"],
          "median_elevation": result["median_elevation"],
          "potential_evapotranspiration_hamon": result["potential_evapotranspiration_hamon"],
          "potential_evapotranspiration_thornthwaite": result["potential_evapotranspiration_thornthwaite"],
          "solar_exposure": result["solar_exposure"],
          "watershed_area": result["watershed_area"],
          "temperature_data": result["temperature_data"]
        }
        
        print("station: {}, watershed: {}, url: {}".format(info["station_number"], info["id"], resp.url))

        watershed_info.append(info)
        writer.writerow(info.values())

        success_count += 1
        log_progress()

log_progress()