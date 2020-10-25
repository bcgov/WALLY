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
headers = {'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJtcGp0Z2tDT2dCVXgydFR2bUFRWFREbTRLLWNYdG5PWVVmM25HZ29OSU5vIn0.eyJleHAiOjE2MDM2ODA1NjYsImlhdCI6MTYwMzY0ODE2NiwiYXV0aF90aW1lIjoxNjAzNjQ4MTY2LCJqdGkiOiJiMjY5YWIwZS1mOTJmLTRmMjEtYTM5Ny05YWI5YjIyYzJkZDIiLCJpc3MiOiJodHRwczovL29pZGMuZ292LmJjLmNhL2F1dGgvcmVhbG1zL2llc3ltZG54IiwiYXVkIjpbIndhbGx5LWdhdGVrZWVwZXIiLCJyZWFsbS1tYW5hZ2VtZW50IiwiYWNjb3VudCJdLCJzdWIiOiJjOGFjM2YyNC04MzlkLTQyM2EtYTRhOS04N2FlZjYwZjI1Y2UiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJ3YWxseS1nYXRla2VlcGVyIiwic2Vzc2lvbl9zdGF0ZSI6IjkwOTdjY2QyLWI4ZDctNDU2NC1hNmNkLWE3MTkwYjVhYmE4YyIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsid2FsbHktbWV0cmljcyIsIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iLCJ3YWxseS12aWV3Il19LCJyZXNvdXJjZV9hY2Nlc3MiOnsicmVhbG0tbWFuYWdlbWVudCI6eyJyb2xlcyI6WyJ2aWV3LXJlYWxtIiwidmlldy1pZGVudGl0eS1wcm92aWRlcnMiLCJtYW5hZ2UtaWRlbnRpdHktcHJvdmlkZXJzIiwicmVhbG0tYWRtaW4iLCJjcmVhdGUtY2xpZW50IiwibWFuYWdlLXVzZXJzIiwicXVlcnktcmVhbG1zIiwidmlldy1hdXRob3JpemF0aW9uIiwicXVlcnktY2xpZW50cyIsInF1ZXJ5LXVzZXJzIiwibWFuYWdlLWV2ZW50cyIsIm1hbmFnZS1yZWFsbSIsInZpZXctZXZlbnRzIiwidmlldy11c2VycyIsInZpZXctY2xpZW50cyIsIm1hbmFnZS1hdXRob3JpemF0aW9uIiwibWFuYWdlLWNsaWVudHMiLCJxdWVyeS1ncm91cHMiXX0sImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJBbGV4IFpvcmtpbiIsInByZWZlcnJlZF91c2VybmFtZSI6ImF6b3JraW5AaWRpciIsImdpdmVuX25hbWUiOiJBbGV4IiwiZmFtaWx5X25hbWUiOiJab3JraW4iLCJlbWFpbCI6ImFsZXhAYmlndGhpbmsuaW8ifQ.XaRUYxCzTg5watmWevQr-DbaeUhcq6zMBDpG32j3mSkcugp2_iuKiizv6-RYq5ZAeGF-vw44o7INvLb9ZWwBSR3niYTzywOGUF8i6pxtOCiRLm7-v4nbTqP6qO9dgCoZsXt_4OSnwtpL2pao4PvEoadeogu0IhZDFLKvi87dg6jt6i-TKvVur0HM-OqMUWt3g-oBobAwVfumx9Hl0V2anOqgc577t_A8ZmW_UqeYPYxFPpSdJWtGP-6YAOotgK7sJAcZG3yJsvJZLJdckHyix39RhUR6j2_gkZI70lgddkZ2OcYXV5hOsC4M-jzbW1Hhk-kp0jzGDek1CI49Ss_9sA'}
# Read in station locations
station_locations_df = pd.read_csv("../output/BC_STATION_LOCATIONS.csv")

# setup output file
date = datetime.datetime.now().strftime('%m-%d-%Y')
filename = "watershed_info" + "_" + date + ".csv"
filepath = "../output/{}".format(filename)

watershed_info = []
resp_error_count = 0
slope_null_count = 0

# gets station info from wally and appends to output csv file on each response if data exists
with open(filepath, "a") as outfile:
    writer=csv.writer(outfile)
    for row in station_locations_df.iterrows():
        station = row[1]
        url = "https://wally.pathfinder.gov.bc.ca/api/v1/watersheds/details/?point=[{},{}]".format(station["LONGITUDE"], station["LATITUDE"])
        resp = req.get(url, headers=headers)
        
        # check for usual bad gateway error and skip
        if resp.status_code != 200:
            print("error url: {}".format(resp.url))
            log.warning(resp.text)
            resp_error_count += 1
            continue
        
        try:
            result = resp.json()
        except:
            log.warning(resp.text)
            continue

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

        # logging row count
        if len(watershed_info) % 50 == 0:
            print("row count: {}".format(len(watershed_info)))

        if info["average_slope"] is None:
            slope_null_count += 1
        
        print("station: {}, slope: {}, url: {}".format(info["station_number"], info["average_slope"], resp.url))

        watershed_info.append(info)
        writer.writerow(info.values())

# Loggin output info
if len(watershed_info) > 0:
    # write stations information to file
    # df = pd.DataFrame(watershed_info)
    # df.to_csv('../output/{}'.format(filename), index=False, header=True)

    # with open("../output/" + filename, "w") as outfile:
    #     json.dump(watershed_info, outfile)
    
    toc = time.time()
    print("process took: {} minutes".format((toc-tic)/60))

    data_size = station_locations_df.size
    failed_call_perc = (resp_error_count / data_size) * 100
    failed_slope_perc = (slope_null_count / data_size) * 100
    success_total = data_size - resp_error_count - slope_null_count
    print("failed calls: {} {}%".format(resp_error_count, failed_call_perc))
    print("slope nulls: {} {}%".format(slope_null_count, failed_slope_perc))
    print("successful stations count: {} out of {}".format(success_total, data_size))
    print("successful stations percentage: {}%".format((success_total / data_size) * 100))
