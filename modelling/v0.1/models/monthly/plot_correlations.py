# -*- coding: utf-8 -*-
import sys
import torch
import json
import pandas as pd
import matplotlib.pyplot as plt


with open('../data/output/training_data/station_flow_training_dataset_08-10-2020.json', 'r') as f:
    data = json.load(f)

filtered_data = [item for item in data if
  item["MONTHLY_MEAN"] != None
]

annual_precipitation = [[item["annual_precipitation"]] for item in filtered_data]
median_elevation = [[item["median_elevation"]] for item in filtered_data]
watershed_area = [[item["watershed_area"]] for item in filtered_data]

y = [[item["MONTHLY_MEAN"]] for item in filtered_data]


plt.clf()
plt.ylabel("MONTLY_MEAN")

plt.subplot(1, 3, 1)
plt.xlabel("annual precipitation")
plt.plot(annual_precipitation, y, 'go', label='True data', alpha=0.1)

plt.subplot(1, 3, 2)
plt.xlabel("median elevation")
plt.plot(median_elevation, y, 'go', label='True data', color='blue', alpha=0.1)

plt.subplot(1, 3, 3)
plt.xlabel("watershed area")
plt.plot(watershed_area, y, 'go', label='True data', color='purple', alpha=0.1)

plt.legend(loc='best')
plt.show()