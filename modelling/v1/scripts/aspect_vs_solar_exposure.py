import pandas as pd
import csv
import seaborn as sns
import matplotlib.pyplot as plt

# filepath = "../data/merged/watersheds_drainage_within_5percent.csv"
# filepath = "../data/4_training/10_year_stations_by_zone_5_percent/25.csv"
filepath = "../data/3_merged/merged_10_year_stations_within_5_percent_drainage_area.csv"


df = pd.read_csv(filepath)

size = (8, 6)

fig_pred, ax1 = plt.subplots(figsize=size)
ax1 = sns.regplot(df['aspect'], df['solar_exposure'], fit_reg=True, truncate=False) 

plt.show()

# indexNames = watershed_stats_df[((watershed_stats_df['drainage_area'] / watershed_stats_df['drainage_area_gross']) - 1).abs() <= 0.05].index
# print(len(watershed_stats_df))
# print(len(indexNames))

# drainage_area_diff = (watershed_stats_df['drainage_area'] / watershed_stats_df['drainage_area_gross'])

# print((drainage_area_diff - 1))

# watersheds_with_5percent_diff = watershed_stats_df.iloc[indexNames]

# watersheds_with_5percent_diff['mean'] = (watersheds_with_5percent_diff['mean'] / watersheds_with_5percent_diff['drainage_area']) * 1000

# print(watersheds_with_5percent_diff[['average_slope', 'mean', 'most_recent_year', 'drainage_area', 'drainage_area_gross', 'latitude', 'longitude', 'average_slope']])

# # export to file
# # watersheds_with_5percent_diff.to_csv(filepath, index=False, header=True)

# # for zone, rows in watershed_stats_df.groupby('hydrological_zone'):
# #     print(rows['aspect'])

