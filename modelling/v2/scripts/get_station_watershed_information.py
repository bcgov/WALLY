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
headers = {'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJzZnFzOG8wZkVhdXMxRWJMNnlkdXY5OUJHbWM3NzdabFpZN05tVG9TVU1jIn0.eyJleHAiOjE2MDU3MDAyNzEsImlhdCI6MTYwNTY2NDI3MSwiYXV0aF90aW1lIjoxNjA1NjY0MjcxLCJqdGkiOiI1YWQ5N2JkZi02YjhiLTQzZDMtODYzZS00MGY1OGVmZDM4MzAiLCJpc3MiOiJodHRwczovL3Rlc3Qub2lkYy5nb3YuYmMuY2EvYXV0aC9yZWFsbXMvaWVzeW1kbngiLCJhdWQiOlsid2FsbHktZ2F0ZWtlZXBlciIsInJlYWxtLW1hbmFnZW1lbnQiLCJhY2NvdW50Il0sInN1YiI6ImJkZWViODQyLTNmYzktNGFiZi1iNTdjLTkyMGRjMzMzODcyOSIsInR5cCI6IkJlYXJlciIsImF6cCI6IndhbGx5LWdhdGVrZWVwZXIiLCJzZXNzaW9uX3N0YXRlIjoiYjI1MjE2ODMtOTEzZi00ZjZjLWJmNWEtOTZmZjA5YjA3Njc0IiwiYWNyIjoiMSIsInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJ3YWxseS1tZXRyaWNzIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsIndhbGx5LXZpZXciXX0sInJlc291cmNlX2FjY2VzcyI6eyJyZWFsbS1tYW5hZ2VtZW50Ijp7InJvbGVzIjpbInZpZXctcmVhbG0iLCJ2aWV3LWlkZW50aXR5LXByb3ZpZGVycyIsIm1hbmFnZS1pZGVudGl0eS1wcm92aWRlcnMiLCJpbXBlcnNvbmF0aW9uIiwicmVhbG0tYWRtaW4iLCJjcmVhdGUtY2xpZW50IiwibWFuYWdlLXVzZXJzIiwicXVlcnktcmVhbG1zIiwidmlldy1hdXRob3JpemF0aW9uIiwicXVlcnktY2xpZW50cyIsInF1ZXJ5LXVzZXJzIiwibWFuYWdlLWV2ZW50cyIsIm1hbmFnZS1yZWFsbSIsInZpZXctZXZlbnRzIiwidmlldy11c2VycyIsInZpZXctY2xpZW50cyIsIm1hbmFnZS1hdXRob3JpemF0aW9uIiwibWFuYWdlLWNsaWVudHMiLCJxdWVyeS1ncm91cHMiXX0sImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJBbGV4IFpvcmtpbiIsInByZWZlcnJlZF91c2VybmFtZSI6ImF6b3JraW5AaWRpciIsImdpdmVuX25hbWUiOiJBbGV4IiwiZmFtaWx5X25hbWUiOiJab3JraW4iLCJlbWFpbCI6ImFsZXhAYmlndGhpbmsuaW8ifQ.bg-lVBTyV3M74-1qXiRCpRK_Nku9E7A2xpPZxREoyiWsVPaJaXAyQK-j5sM4RojNXeYde7FhaxEvd3ipleNVozERg7-JqznvUpXd13QSOD_O5c4SZMbkAPBQI93nvhMhKourIgOUKj_p01BpbEScknysPsIwMUck4e_3R_sFss832tc10z3eExaWRcYJKmA_XGaOUxywxqFdW0i9lws2KmFA0xiTshkiFtw_FM9oz8uF-1um5tuIrUHDQV5AD-bECGjBWLkh-Yy8yTvwTKXMweSSChaE2JZgjypTn240jsLmulMDjWOWK0r8AFzKwk1KociPIrF1gstQZaGcE22eWg'}
# Read in station locations
station_locations_df = pd.read_csv("../data/bc_station_locations/bc_station_locations_nov16.csv")
existing_stations_df = pd.read_csv("../data/station_watershed_info_11-16-2020.csv")
existing_stations_list = existing_stations_df["station_number"].tolist()

# setup output file
# date = datetime.datetime.now().strftime('%m-%d-%Y')
# filename = "station_watershed_info" + "_" + date + ".csv"
# filepath = "../data/{}".format(filename)

filepath = "../data/station_watershed_info_11-16-2020.csv"

watershed_info = []
row_count = 0
already_exists_count = 0
success_count = 0
resp_error_count = 0
slope_null_count = 0


def log_progress():
    # if(len(watershed_info) <= 0):
    #     print("no watershed info")
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
    print("already existing stations: {}/{}%".format(already_exists_count, len(existing_stations_list)))
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

        if station["STATION_NUMBER"] in existing_stations_list:
            print("station data already exists")
            already_exists_count += 1
            continue

        url = "https://wally-staging.pathfinder.gov.bc.ca/api/v1/watersheds/details/?point=[{},{}]".format(station["LONGITUDE"], station["LATITUDE"])
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