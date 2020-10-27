#!/usr/bin/env python3

import requests as req
import csv 
import json
import time
import datetime

tic = time.time()

# Add Wally access token here
headers = {'Authorization': 'Bearer <access_token>'}

with open('../../output/stations/station_watershed_info_08-10-2020.json') as json_file:
    data = json.load(json_file)
    
    watershed_characteristics = []
    resp_error_count = 0
    slope_null_count = 0

    for station in data:
        resp = req.get("https://wally-staging.pathfinder.gov.bc.ca/api/v1/watersheds/" + station["id"], headers=headers)
        
        # check for usual bad gateway error and skip
        if resp.status_code != 200:
            print("error url: {}".format(resp.url))
            resp_error_count += 1
            continue
        
        result = resp.json()

        inputs = {
          "id": station["id"],
          "STATION_NUMBER": station["STATION_NUMBER"],
          "DRAINAGE_AREA_GROSS": station["DRAINAGE_AREA_GROSS"],
          "LATITUDE": station["LATITUDE"],
          "LONGITUDE": station["LONGITUDE"],
          "FEATURE_AREA_SQM": station["FEATURE_AREA_SQM"],
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

        # logging row count
        if len(watershed_characteristics) % 50 == 0:
            print("row count: {}".format(len(watershed_characteristics)))

        if inputs["average_slope"] is None:
            slope_null_count += 1
        
        print("station: {}, slope: {}, url: {}".format(inputs["STATION_NUMBER"], inputs["average_slope"], resp.url))

        watershed_characteristics.append(inputs)
    
    if len(watershed_characteristics) > 0:
        date = datetime.datetime.now().strftime('%m-%d-%Y')
        filename = "station_watershed_characteristics" + "_" + date + ".json"

        # write stations information to file
        with open("../../output/stations/" + filename, "w") as outfile:
            json.dump(watershed_characteristics, outfile)
        
        toc = time.time()
        print("process took: {} minutes".format((toc-tic)/60))

        data_size = len(data)
        failed_call_perc = (resp_error_count / data_size) * 100
        failed_slope_perc = (slope_null_count / data_size) * 100
        success_total = data_size - resp_error_count - slope_null_count
        print("failed calls: {} {}%".format(resp_error_count, failed_call_perc))
        print("slope nulls: {} {}%".format(slope_null_count, failed_slope_perc))
        print("successful stations count: {} out of {}".format(success_total, data_size))
        print("successful stations percentage: {}%".format((success_total / data_size) * 100))
