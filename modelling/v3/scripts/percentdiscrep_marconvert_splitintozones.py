import pandas as pd
import csv

# import data
df = pd.read_csv("../data/2_scrape_results/watershed_stats_output_06_30_2021-23_38_57.csv")

# 5 percent discrepancy
indexNames = df[((df['drainage_area'] / df['drainage_area_gross']) - 1).abs() <= 0.2].index
df = df.iloc[indexNames]

# Mar adjustment
df['mean'] = (df['mean'] / df['drainage_area']) * 1000

print(df[['station_number','latitude', 'longitude', 'drainage_area', 'drainage_area_gross']])

# export to files
output_directory = "jun30"

for zone, rows in df.groupby('hydrological_zone'):
    rows.to_csv(f'../data/4_training/{output_directory}/{round(zone)}.csv', index=False, header=True)
