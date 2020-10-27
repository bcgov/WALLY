import json
import time
import datetime
import pandas as pd

tic = time.time()

watershed_info_df = pd.read_csv("../data/station_watershed_info_10-25-2020.csv")
mean_annual_flows_df = pd.read_csv("../data/bc_mean_annual_flows/bc_mean_annual_flows.csv")

training_set = []
null_station_ids = set()
hydrological_zones = {}
not_found = []
found_stations = {}

# testing
# mean_annual_flows_df = mean_annual_flows_df.head(1000)

for record in mean_annual_flows_df.iterrows():
    record = record[1].to_dict()
    station_number = record["STATION_NUMBER"]
    if station_number in not_found:
        continue
    if station_number in found_stations.keys():
        station = found_stations[station_number]
    else:
        station = next((wd[1].to_dict() for wd in watershed_info_df.iterrows() if wd[1][1] == station_number), None)
    if station is None:
        print("FOUND NO STATION: {}".format(station_number))
        null_station_ids.add(station_number)
        not_found.append(station_number)
    if station:
        # station_number,year,mean,min_month,min,max_month,max,average_slope,temperature_data,glacial_coverage,glacial_area,watershed_area,potential_evapotranspiration_thornthwaite,potential_evapotranspiration_hamon,hydrological_zone,annual_precipitation,median_elevation,aspect,solar_exposure,latitude,longitude,drainage_area
        record_info = {
          "station_number": station_number,
          "year": record["YEAR"],
          "mean": record["MEAN"],
          "min_month": record["MIN_MONTH"],
          "min": record["MIN"],
          "max_month": record["MAX_MONTH"],
          "max": record["MAX"],
        }
        station_info = {
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
          "latitude": station["latitude"],
          "longitude": station["longitude"],
          "drainage_area": station["drainage_area"]
        }
        training_item = {
          **record_info,
          **station_info
        }
        found_stations[station_number] = station_info
        training_set.append(training_item)
        
        print("STATION FOUND: {}".format(training_item["station_number"]))

        zone = training_item["hydrological_zone"]
        if not hydrological_zones.get(zone, None):
            hydrological_zones[zone] = []
        hydrological_zones[zone].append(training_item)


for key in hydrological_zones:
    print("zone {} -> {}".format(key, len(hydrological_zones[key])))
    df = pd.DataFrame(hydrological_zones[key])
    keyname = '0' + str(key) if key < 10 else key
    df.to_csv('../data/training_data_hydro_zone_annual_flow/zone_{}.csv'.format(keyname), index=False, header=True)


# log outcome
print("writing file with {} items".format(len(training_set)))
print("No station count: {}".format(len(list(null_station_ids))))

toc = time.time()
print("process took: {} minutes".format((toc-tic)/60))
