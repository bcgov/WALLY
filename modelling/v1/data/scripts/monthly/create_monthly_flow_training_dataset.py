import json
import time
import datetime

watershed_data = []
flow_data = []
tic = time.time()

with open('../../output/stations/station_watershed_characteristics_08-10-2020.json') as watershed_file:
    watershed_data = json.load(watershed_file)

with open('../../output/flow/station_flow_values_08-10-2020.json') as flow_file:
    flow_data = json.load(flow_file)

training_set = []

for flow in flow_data:
    station = next((wd for wd in watershed_data if wd["STATION_NUMBER"] == flow["STATION_NUMBER"]), None)
    if station and station["average_slope"]: # filter out any stations that we didn't get SEA info for
        training_item = {
          "STATION_NUMBER": flow["STATION_NUMBER"],
          "MONTHLY_TOTAL": flow["MONTHLY_TOTAL"], 
          "MIN": flow["MIN"], 
          "MAX": flow["MAX"], 
          "MONTH": flow["MONTH"], 
          "MONTHLY_MEAN": flow["MONTHLY_MEAN"], 
          "YEAR": flow["YEAR"], 
          "NO_DAYS": flow["NO_DAYS"],
          "average_slope": station["average_slope"], 
          "temperature_data": station["temperature_data"], 
          "glacial_coverage": station["glacial_coverage"], 
          "glacial_area": station["glacial_area"], 
          "watershed_area": station["watershed_area"], 
          "potential_evapotranspiration_thornthwaite": station["potential_evapotranspiration_thornthwaite"], 
          "potential_evapotranspiration_hamon": station["potential_evapotranspiration_hamon"],
          "hydrological_zone": station["hydrological_zone"], 
          "annual_precipitation": station["annual_precipitation"], 
          "median_elevation": station["median_elevation"], 
          "aspect": station["aspect"], 
          "solar_exposure": station["solar_exposure"], 
          "LATITUDE": station["LATITUDE"], 
          "LONGITUDE": station["LONGITUDE"], 
          "drainage_area": station["drainage_area"],
          "DRAINAGE_AREA_GROSS": station["DRAINAGE_AREA_GROSS"], 
          "FEATURE_AREA_SQM": station["FEATURE_AREA_SQM"]
        }
        training_set.append(training_item)

if len(training_set) > 0:
    date = datetime.datetime.now().strftime('%m-%d-%Y')
    filename = "station_flow_training_dataset" + "_" + date + ".json"
    print("writing file with {} items".format(len(training_set)))
    # write dataset to file
    with open("../../output/training_data/" + filename, "w") as outfile:
        json.dump(training_set, outfile)
    
    toc = time.time()
    print("process took: {} minutes".format((toc-tic)/60))
