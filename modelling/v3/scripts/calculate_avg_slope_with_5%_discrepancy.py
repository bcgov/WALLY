import pandas as pd
import csv
import math
import numpy as np

input_file_path = "../data/2_scrape_results/watershed_stats_output_by_station_id.csv"
output_file_path = "../data/2_scrape_results/watershed_stats_modified_slope.csv"

watershed_stats_df = pd.read_csv(input_file_path)

# updated slope to fit less than 45 percent
slope = watershed_stats_df["average_slope"]
slope = slope.div(100)
slope = np.arctan(slope)
slope = np.rad2deg(slope)
slope = np.abs(slope)
slope = slope.div(2)
print(slope)
print(slope.max())
watershed_stats_df['average_slope'] = slope

# over 5% discrepancies in drainage area removed
indexNames = watershed_stats_df[((watershed_stats_df['drainage_area'] / watershed_stats_df['drainage_area_gross']) - 1).abs() <= 0.05].index
watersheds_with_5percent_diff = watershed_stats_df.iloc[indexNames]
watersheds_with_5percent_diff['mean'] = (watersheds_with_5percent_diff['mean'] / watersheds_with_5percent_diff['drainage_area']) * 1000

watersheds_with_5percent_diff.to_csv(output_file_path, index=False, header=True)
