# -*- coding: utf-8 -*-
import sys
import torch
import json
import pandas as pd
import matplotlib.pyplot as plt


with open('../../data/output/training_data/annual_mean_training_dataset_08-11-2020.json', 'r') as f:
    data = json.load(f)

filtered_data = [item for item in data 
# if item["YEAR"] == 2018 and
  if item["MEAN"] < 1500 and
  item["drainage_area"] < 150 and
  item["annual_precipitation"] < 6000
]

print(len(filtered_data))

annual_precipitation = [[item["annual_precipitation"]] for item in filtered_data]
median_elevation = [[item["median_elevation"]] for item in filtered_data]
drainage_area = [[item["drainage_area"]] for item in filtered_data]
avg_temp = [[sum([monthTemps[2] for monthTemps in item["temperature_data"]]) / 12] for item in filtered_data]
year = [[item["YEAR"]] for item in filtered_data]

y = [[item["MEAN"]] for item in filtered_data]

plt.clf()
plt.suptitle('Mean Annual Flow vs Independant Variables', fontsize=16)

plt.subplot(1, 5, 1)
plt.xlabel("annual precipitation (mm)")
plt.plot(annual_precipitation, y, 'go', label='True data', alpha=0.1)
plt.ylabel('Mean Annual Flow (m3/s)')

plt.subplot(1, 5, 2)
plt.xlabel("median elevation (m)")
plt.plot(median_elevation, y, 'go', label='True data', color='blue', alpha=0.1)

plt.subplot(1, 5, 3)
plt.xlabel("drainage area (km2)")
plt.plot(drainage_area, y, 'go', label='True data', color='purple', alpha=0.1)

plt.subplot(1, 5, 4)
plt.xlabel("avg temp")
plt.plot(avg_temp, y, 'go', label='True data', color='orange', alpha=0.1)

plt.subplot(1, 5, 5)
plt.xlabel("year")
plt.plot(year, y, 'go', label='True data', color='red', alpha=0.1)

plt.legend(loc='best')
plt.show()