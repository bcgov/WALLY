import os
import json
import time
import datetime
import pandas as pd

tic = time.time()

directory = '../data/bc_dly_monthly_flows/'

watershed_info_df = pd.read_csv("../data/station_watershed_info_10-25-2020.csv")
# monthly_distributions_df = pd.read_csv("../data/bc_dly_monthly_flows/bc_dly_monthly_flows.csv")

training_set = []
null_station_ids = set()
hydrological_zone_months = {}
not_found = []
found_stations = {}

# testing
# monthly_distributions_df = monthly_distributions_df.head(1000)

for filename in sorted(os.listdir(directory)):
    if filename.endswith(".csv"):
        monthly_distributions_df = pd.read_csv(os.path.join(directory, filename))

        for record in monthly_distributions_df.iterrows():
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
                # "STATION_NUMBER","YEAR","MONTH","NO_DAYS","MONTHLY_MEAN","MONTHLY_TOTAL","MIN","MAX","DRAINAGE_AREA_GROSS","DRAINAGE_AREA_EFFECT","LATITUDE","LONGITUDE"
                record_info = {
                  "station_number": station_number,
                  "year": record["YEAR"],
                  "month": record["MONTH"],
                  "num_days": record["NO_DAYS"],
                  "monthly_mean": record["MONTHLY_MEAN"],
                  "monthly_total": record["MONTHLY_TOTAL"],
                  "min": record["MIN"],
                  "max": record["MAX"]
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
                month = training_item["month"]
                if not hydrological_zone_months.get(zone, None):
                    hydrological_zone_months[zone] = {}
                if not hydrological_zone_months[zone].get(month, None):
                    hydrological_zone_months[zone][month] = []

                hydrological_zone_months[zone][month].append(training_item)


for zone in hydrological_zone_months:
    for month in hydrological_zone_months[zone]:
        print("zone {} month {} -> {}".format(zone, month, len(hydrological_zone_months[zone][month])))
        df = pd.DataFrame(hydrological_zone_months[zone][month])
        # keyname = '0' + str(month) if month < 10 else zone
        df.to_csv('../data/training_data_hydro_zone_monthly_distributions/zone_{}/{}.csv'.format(zone, month), index=False, header=True)


# log outcome
print("writing file with {} items".format(len(training_set)))
print("No station count: {}".format(len(list(null_station_ids))))

toc = time.time()
print("process took: {} minutes".format((toc-tic)/60))
