#!/usr/bin/env python3

# This script gets watershed information from 
# any lat long that you provide in the point parameter
# The id field is used in the next stage to get 
# watershed characteristics

import requests as req
import csv 
import json
import time
import datetime

# Add Wally access token here
headers = {'Authorization': 'Bearer <access_token>'}

with open('../../output/db/annual_statistics_stations_bc_gte2000.json') as json_file:
    data = json.load(json_file)
    
    tic = time.time()
    stations_output = []
    geometries_output = []

    for station in data:
        params = {
          'point': '[{},{}]'.format(station["LONGITUDE"], station["LATITUDE"])
        }
        
        resp = req.get("https://wally-staging.pathfinder.gov.bc.ca/api/v1/watersheds/", params=params, headers=headers)
        
        # check for usual bad gateway error and skip
        if resp.status_code != 200:
            print("error url: {}".format(resp.url))
            continue
        
        feature_collection = resp.json()
        # pluck out generated watershed feature
        feature = feature_collection["features"][0]
        
        # merge together station info and generated watershed info
        station_data = {
          "STATION_NUMBER": station["STATION_NUMBER"],
          "STATION_NAME": station["STATION_NAME"],
          "DRAINAGE_AREA_GROSS": station["DRAINAGE_AREA_GROSS"],
          "LATITUDE": station["LATITUDE"],
          "LONGITUDE": station["LONGITUDE"],
          'id': feature["id"],
          'FEATURE_AREA_SQM': feature["properties"]["FEATURE_AREA_SQM"],
          'source_url': resp.url
        }

        # separate out actual geometry data to save working memory later on
        watershed_geometry = {
          "STATION_NUMBER": station["STATION_NUMBER"],
          'geometry': feature["geometry"]
        }

        # logging row count
        if len(stations_output) % 50 == 0:
            print("row count: {}".format(len(stations_output)))

        print("station: {} id: {} url: {}".format(station_data["STATION_NUMBER"], station_data["id"], resp.url))

        stations_output.append(station_data)
        geometries_output.append(watershed_geometry)
    
    if len(stations_output) > 0:
        date = datetime.datetime.now().strftime('%m-%d-%Y')
        info_filename = "station_watershed_info" + "_" + date + ".json"
        geometry_filename = "station_watershed_geometry" + "_" + date + ".json"

        # write stations information to file
        with open("../../output/stations/annual/" + info_filename, "w") as outfile:
            json.dump(stations_output, outfile)
        
        # write stations geometry in a different file to save working memory space
        with open("../../output/stations/annual/" + geometry_filename, "w") as outfile:
            json.dump(geometries_output, outfile)
        
        toc = time.time()
        print("process took: {} seconds".format(toc-tic))
