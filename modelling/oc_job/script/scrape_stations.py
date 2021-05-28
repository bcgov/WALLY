#!/usr/bin/env python3

import os
import requests as req
import csv 
import time
import pandas as pd
from minio import Minio
# from dotenv import load_dotenv
# load_dotenv()

tic = time.time()

MINIO_HOST_URL = os.getenv("MINIO_HOST_URL", "")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "")
BUCKET_NAME = 'modelling'

# Add Wally access token here
headers = {
  'X-Auth-Subject': '00000000-0000-0000-0000-000000000000',
  'X-Auth-Email': 'dev.wally.test@gov.bc.ca',
  'X-Auth-Roles': '',
  'X-Auth-Userid': 'dev@idir'
}

minio_client = Minio(MINIO_HOST_URL,
                  access_key=MINIO_ACCESS_KEY,
                  secret_key=MINIO_SECRET_KEY,
                  secure=False)

# MINIO GET
def get_minio_file(object_name):
    try:
        result = minio_client.get_object(BUCKET_NAME, object_name)
        return result
    except Exception as exc:
        print('error getting file: ', exc)

local_file_path = "./watershed_stats_output.csv"

# MINIO PUT
def put_minio_file(object_name):
    try:
        result = minio_client.fput_object(bucket_name=BUCKET_NAME,
                                          object_name=object_name,
                                          file_path=local_file_path,
                                          content_type='csv')
    except Exception as exc:
        print('error putting file: ', exc)


object_name = 'bc_mean_annual_flows_flattened.csv'
bc_mean_annual_flows = get_minio_file(object_name)

# Read in station locations
stations_df = pd.read_csv(bc_mean_annual_flows)
print(stations_df)

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
    print("failed calls: {} {}%".format(resp_error_count, failed_call_perc))
    print("successful watersheds count: {} out of {}".format(success_count + already_exists_count, row_count))
    print("successful watersheds percentage: {}%".format((success_count / row_count) * 100))
    print("*** LOG END ***")


# gets station info from wally and appends to output csv file on each response if data exists
with open(local_file_path, "a") as outfile:
    writer=csv.writer(outfile)
    for row in stations_df.iterrows():
        row_count += 1
        station = row[1]

        station_id = "hydat." + station["STATION_NUMBER"]

        base_url = "http://wally-staging-api:8000"
        # base_url = "https://wally-staging.apps.silver.devops.gov.bc.ca"
        resp = req.get(base_url + "/api/v1/watersheds/" + station_id, headers=headers)
        
        # check for usual bad gateway error and skip
        if resp.status_code != 200:
            print("error: {}".format(resp.url))
            try:
                print(resp.json())
            except:
                print(resp.text)
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
        
        # station_number,most_recent_year,years_of_data,mean,min,max,drainage_area_gross,latitude,longitude,gen_id,annual_precipitation,aspect,average_slope,drainage_area,glacial_area,glacial_coverage,hydrological_zone,median_elevation,potential_evapotranspiration_hamon,potential_evapotranspiration_thornthwaite,solar_exposure,watershed_area,temperature_data
        info = {
          "station_number": station["STATION_NUMBER"],
          "most_recent_year": station["YEAR"],
          "years_of_data": station["YEARS_OF_DATA"],
          "mean": station["MEAN"],
          "min": station["MIN"],
          "max": station["MAX"],
          "drainage_area_gross": station["DRAINAGE_AREA_GROSS"],
          "latitude": station["LATITUDE"],
          "longitude": station["LONGITUDE"],

          "gen_id": result["watershed_id"],
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
        
        print("success: {}".format(resp.url))

        watershed_info.append(info)
        writer.writerow(info.values())

        success_count += 1
        log_progress()

put_minio_file("watershed_stats_output.csv")

log_progress()
print(headers)