#!/usr/bin/env python3

import os
import requests as req
import csv 
import time
import pandas as pd
from minio import Minio
from datetime import date, datetime
# from dotenv import load_dotenv
# load_dotenv()

allowed_station_ids = ['08FB001','08FB006','08FB007','08GD005','08GD006','08GD007','08GD009','08GE001','08GE002','08LG008','08LG010','08LG048','08LG068','08MA002','08ME004','08ME005','08ME011','08ME022','08ME027','08ME028','08MF008','08MF062','08MF065','08MG005','08MG008','08NL007','08NL008','08NL023','08NL024','08NL060','08NL067','08NL070','08NL071','08FA002','08FB003','08FB004','08FB005','08FB009','08GA017','08GA022','08GA023','08GA024','08GA043','08GA054','08GA057','08GA071','08GA072','08GA075','08GB009','08GB013','08GC003','08GE003','08GF001','08GF008','08MF002','08MF003','08MF009','08MF030','08MF031','08MF032','08MF034','08MF048','08MF068','08MG003','08MG004','08MG006','08MG007','08MG009','08MG013','08MG025','08MG026','08MH017','08MH055','08MH103','08MH147','08PA001','08PA002','08FA001','08FA002','08FA004','08FA005','08FA006','08FA007','08FD002','08GF001','08GF004','08GF005','08GF006','08GF007','08GF008','08GF009','08GA001','08GA002','08GA003','08GA004','08GA005','08GA006','08GA007','08GA008','08GA009','08GA010','08GA011','08GA012','08GA013','08GA015','08GA018','08GA019','08GA021','08GA025','08GA026','08GA027','08GA028','08GA030','08GA031','08GA049','08GA052','08GA059','08GA061','08GA062','08GA063','08GA065','08GA068','08GA076','08GA077','08GA079','08MH002','08MH003','08MH004','08MH005','08MH006','08MH010','08MH018','08MH019','08MH020','08MH021','08MH022','08MH026','08MH035','08MH046','08MH050','08MH059','08MH060','08MH061','08MH069','08MH089','08MH090','08MH092','08MH097','08MH104','08MH105','08MH107','08MH112','08MH117','08MH123','08MH126','08MH129','08MH134','08MH139','08MH141','08MH146','08MH149','08MH151','08MH154','08MH155','08MH166','08MH168','08MF018','08MF036','08MF048','08MF049','08MF054','08MF059','08MF061','08MF064','08MF073','08MG001','08MG009','08MG014','08MG022','08MG023','08MH001','08MH008','08MH009','08MH011','08MH012','08MH014','08MH024','08MH029','08MH031','08MH033','08MH037','08MH045','08MH047','08MH049','08MH051','08MH058','08MH068','08MH070','08MH071','08MH072','08MH073','08MH074','08MH075','08MH076','08MH077','08MH079','08MH080','08MH081','08MH082','08MH083','08MH084','08MH085','08MH086','08MH088','08MH091','08MH093','08MH094','08MH095','08MH096','08MH098','08MH099','08MH100','08MH108','08MH125','08MH130','08MH131','08MH133','08MH138','08MH145','08MH147','08MH148','08MH150','08MH152','08MH153','08MH156','08MH157','08MH167','08GA020','08GA036','08GA037','08GA045','08GA046','08GA047','08GA050','08GA051','08GA060','08GA069','08GA070','08GA078','08GB003','08GB005','08GB006','08GB007','08GB008','08GB009','08GB010','08GB011','08GB012','08GB013','08GB014','08GC004','08GC005','08GC006','08GC007','08GC008','08GF003','08HD017']

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
local_licence_file_path = "./watershed_licence_output.csv"
local_approvals_file_path = "./watershed_approvals_output.csv"

# MINIO PUT
def put_minio_file(object_name, path):
    try:
        result = minio_client.fput_object(bucket_name=BUCKET_NAME,
                                          object_name=object_name,
                                          file_path=path,
                                          content_type='csv')
    except Exception as exc:
        print('error putting file: ', exc)


object_name = 'bc_mean_annual_flows_flattened.csv'
bc_mean_annual_flows = get_minio_file(object_name)

# Read in station locations
stations_df = pd.read_csv(bc_mean_annual_flows)
print(stations_df)

row_count = 0
already_exists_count = 0
success_count = 0
resp_error_count = 0


def log_progress():
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

        if station["STATION_NUMBER"] not in allowed_station_ids:
            continue

        station_id = "hydat." + station["STATION_NUMBER"]

        base_url = "http://wally-staging-api:8000"
        station_url = base_url + "/api/v1/watersheds/" + station_id
        # base_url = "https://wally-staging.apps.silver.devops.gov.bc.ca"
        
        for i in range(0,3):
            try:
                resp = req.get(station_url, headers=headers)
            except:
                print('watershed request failed:', resp.url)
            # retry call if failed after 1 second
            if resp.status_code != 200:
                print("error: {}".format(resp.url))
                time.sleep(1)
                continue
            else:
                break

        # check for usual bad gateway error and skip
        if resp.status_code != 200:
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
        
        # station_number,most_recent_year,years_of_data,mean,min,max,drainage_area_gross,latitude,longitude,gen_id,annual_precipitation,aspect,average_slope,drainage_area,glacial_area,glacial_coverage,hydrological_zone,median_elevation,potential_evapotranspiration,solar_exposure,watershed_area
        watershed_info = {
          "station_number": station["STATION_NUMBER"],
          "most_recent_year": station["YEAR"],
          "years_of_data": station["YEARS_OF_DATA"],
          "mean": station["MEAN"],
          "min": station["MIN"],
          "max": station["MAX"],
          "drainage_area_gross": station["DRAINAGE_AREA_GROSS"],
          "latitude": station["LATITUDE"],
          "longitude": station["LONGITUDE"],

          "gen_id": result["generated_watershed_id"],
          "annual_precipitation": result["annual_precipitation"],
          "aspect": result["aspect"],
          "average_slope": result["average_slope"],
          "drainage_area": result["drainage_area"],
          "glacial_area": result["glacial_area"],
          "glacial_coverage": result["glacial_coverage"],
          "hydrological_zone": result["hydrological_zone"],
          "median_elevation": result["median_elevation"],
          "potential_evapotranspiration": result["potential_evapotranspiration"],
          "solar_exposure": result["solar_exposure"],
          "watershed_area": result["watershed_area"]
        }
        
        writer.writerow(watershed_info.values())
        print("watershed success: {}".format(resp.url))

        # Station watershed licenced use information
        with open(local_licence_file_path, "a") as licence_outfile:
            licence_writer = csv.writer(licence_outfile)
            licence_url = station_url + '/licences?generated_watershed_id=' + watershed_info["gen_id"]
            for i in range(0,3):
                try:
                    resp = req.get(licence_url, headers=headers)
                except:
                    print('licence request failed:', resp.url)
                # retry call if failed after 1 second
                if resp.status_code != 200:
                    print("error: {}".format(resp.url))
                    time.sleep(1)
                    continue
                else:
                    break
            try:
                licence_result = resp.json()
            except:
                print(resp.text)
                continue

            if licence_result is None:
                print("licence result is null")
            
            licence_info = {
              "station_number": station["STATION_NUMBER"],
              "gen_id": watershed_info["gen_id"],
              **licence_result
            }
            
            print("licence success: {}".format(resp.url))
            licence_writer.writerow(licence_info.values())

        # Station watershed approvals use information
        with open(local_approvals_file_path, "a") as approvals_outfile:
            approvals_writer = csv.writer(approvals_outfile)
            approvals_url = station_url + '/approvals?generated_watershed_id=' + watershed_info["gen_id"]
            for i in range(0,3):
                try:
                    resp = req.get(approvals_url, headers=headers)
                except:
                    print('approvals request failed:', resp.url)
                # retry call if failed after 1 second
                if resp.status_code != 200:
                    print("error: {}".format(resp.url))
                    time.sleep(1)
                    continue
                else:
                    break
            try:
                approvals_result = resp.json()
            except:
                print(resp.text)
                continue

            if approvals_result is None:
                print("approvals result is null")
            
            approvals_info = {
              "station_number": station["STATION_NUMBER"],
              "gen_id": watershed_info["gen_id"],
              **approvals_result
            }
            
            print("approvals success: {}".format(resp.url))
            approvals_writer.writerow(approvals_info.values())

        success_count += 1
        log_progress()

now = datetime.now()
date_time = now.strftime("%m:%d:%Y-%H:%M:%S")
put_minio_file("watershed_stats_output_{}.csv".format(date_time), local_file_path)
put_minio_file("watershed_licence_output_{}.csv".format(date_time), local_licence_file_path)
put_minio_file("watershed_approvals_output_{}.csv".format(date_time), local_approvals_file_path)

log_progress()
print(headers)

