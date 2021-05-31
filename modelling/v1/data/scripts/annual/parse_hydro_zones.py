import json
import time
import datetime
import pandas as pd

tic = time.time()

hydrological_zones = {}

with open('../../output/training_data/annual_mean_training_dataset_08-11-2020.json') as training_data:
    data = json.load(training_data)

    for station in data:
        zone = station["hydrological_zone"]
        if not hydrological_zones.get(zone, None):
            hydrological_zones[zone] = []

        hydrological_zones[station["hydrological_zone"]].append(station)

    for key in hydrological_zones:
        print("zone {} -> {}".format(key, len(hydrological_zones[key])))
        df = pd.DataFrame(hydrological_zones[key])
        keyname = '0' + str(key) if key < 10 else key
        df.to_csv('../../output/hydrological_zones/zone_{}.csv'.format(keyname), index=False, header=True)