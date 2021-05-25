import json
import time
import datetime

tic = time.time()

watershed_data = []
annual_data = []

with open('../../output/stations/station_watershed_characteristics_08-10-2020.json') as watershed_file:
    watershed_data = json.load(watershed_file)

with open('../../output/stations/annual/station_watershed_characteristics_fetched_missing_08-11-2020.json') as missing_watershed_file:
    missing_watershed_data = json.load(missing_watershed_file)

with open('../../output/db/annual_statistics_mean_bc_gte2000.json') as annual_file:
    annual_data = json.load(annual_file)

training_set = []
null_station_ids = set()

for record in annual_data:
    station = next((wd for wd in watershed_data if wd["STATION_NUMBER"] == record["STATION_NUMBER"]), None)
    if station is None:
        station = next((md for md in missing_watershed_data if md["STATION_NUMBER"] == record["STATION_NUMBER"]), None)
        if station is None:
            print("FOUND NO STATION: {}".format(record["STATION_NUMBER"]))
            null_station_ids.add(record["STATION_NUMBER"])
    if station:
        training_item = {
          "STATION_NUMBER": record["STATION_NUMBER"],
          "YEAR": record["YEAR"],
          "MEAN": record["MEAN"],
          "MIN_MONTH": record["MIN_MONTH"],
          "MIN": record["MIN"],
          "MAX_MONTH": record["MAX_MONTH"],
          "MAX": record["MAX"],
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
    filename = "annual_mean_training_dataset" + "_" + date + ".json"
    print("writing file with {} items".format(len(training_set)))
    # write dataset to file
    with open("../../output/training_data/" + filename, "w") as outfile:
        json.dump(training_set, outfile)
    
    with open("../../output/training_data/missing_station_ids.json", "w") as outfile:
        json.dump(list(null_station_ids), outfile)
    
    print("No station count: {}".format(len(list(null_station_ids))))

    toc = time.time()
    print("process took: {} minutes".format((toc-tic)/60))
