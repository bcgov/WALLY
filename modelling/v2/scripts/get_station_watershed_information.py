#!/usr/bin/env python3

import requests as req
import csv 
import time
import datetime
import logging
import pandas as pd
from pathlib import Path

log = logging.getLogger(__name__)

tic = time.time()

# Add Wally access token here
headers = {'Authorization': 'Bearer <token>'}
# Read in station locations
station_locations_df = pd.read_csv("../data/bc_station_locations/bc_station_locations.csv")

# setup output file
date = datetime.datetime.now().strftime('%m-%d-%Y')
filename = "station_watershed_info" + "_" + date + ".csv"
filepath = "../data/{}".format(filename)

watershed_info = []
row_count = 0
success_count = 0
resp_error_count = 0
slope_null_count = 0


def log_progress():
    if(len(watershed_info) <= 0):
        print("no watershed info")
    if row_count % 30 != 0:
        return

    print("*** LOG PROGRESS ***")
    print("row count: {}".format(row_count))

    toc = time.time()
    print("process time: {} minutes".format((toc-tic)/60))

    # data_size = station_locations_df.size
    failed_call_perc = (resp_error_count / row_count) * 100
    failed_slope_perc = (slope_null_count / row_count) * 100
    # success_total = data_size - resp_error_count - slope_null_count
    print("failed calls: {} {}%".format(resp_error_count, failed_call_perc))
    print("slope nulls: {} {}%".format(slope_null_count, failed_slope_perc))
    print("successful stations count: {} out of {}".format(success_count, row_count))
    print("successful stations percentage: {}%".format((success_count / row_count) * 100))
    print("*** LOG END ***")


# gets station info from wally and appends to output csv file on each response if data exists
with open(filepath, "a") as outfile:
    writer=csv.writer(outfile)
    for row in station_locations_df.iterrows():
        row_count += 1
        station = row[1]
        url = "https://wally.pathfinder.gov.bc.ca/api/v1/watersheds/details/?point=[{},{}]".format(station["LONGITUDE"], station["LATITUDE"])
        resp = req.get(url, headers=headers)
        
        # check for usual bad gateway error and skip
        if resp.status_code != 200:
            print("error url: {}".format(resp.url))
            resp_error_count += 1
            log_progress()
            continue
        
        try:
            result = resp.json()
        except:
            log.warning(resp.text)
            continue
        # id,station_number,latitude,longitude,watershed_area,drainage_area,glacial_area,glacial_coverage,temperature_data,annual_precipitation,potential_evapotranspiration_hamon,potential_evapotranspiration_thornthwaite,hydrological_zone,average_slope,solar_exposure,median_elevation,aspect
        info = {
          "id": result["watershed_id"],
          "station_number": station["STATION_NUMBER"],
          "latitude": station["LATITUDE"],
          "longitude": station["LONGITUDE"],
          "watershed_area": result["watershed_area"],
          "drainage_area": result["drainage_area"],
          "glacial_area": result["glacial_area"],
          "glacial_coverage": result["glacial_coverage"],
          "temperature_data": result["temperature_data"],
          "annual_precipitation": result["annual_precipitation"],
          "potential_evapotranspiration_hamon": result["potential_evapotranspiration_hamon"],
          "potential_evapotranspiration_thornthwaite": result["potential_evapotranspiration_thornthwaite"],
          "hydrological_zone": result["hydrological_zone"],
          "average_slope": result["average_slope"],
          "solar_exposure": result["solar_exposure"],
          "median_elevation": result["median_elevation"],
          "aspect": result["aspect"]
        }

        if info["average_slope"] is None:
            slope_null_count += 1
        
        print("station: {}, slope: {}, url: {}".format(info["station_number"], info["average_slope"], resp.url))

        watershed_info.append(info)
        writer.writerow(info.values())

        success_count += 1
        log_progress()

log_progress()