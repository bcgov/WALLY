
import pandas as pd
import csv

# pd.set_option('display.max_columns', None)

# import station data and watershed stats as dataframes
# stations_df = pd.read_csv("../../data/1_source/yearly_stations_flattened/bc_mean_annual_flows_10_year_stations.csv")
stations_df = pd.read_csv("../../data/1_source/yearly_stations_flattened/bc_mean_annual_flows_20_year_stations.csv")
watersheds_df = pd.read_csv("../../data/2_scrape_results/watershed_stats.csv")

# set station column names to lower case
stations_df.columns = stations_df.columns.str.lower()

# print(stations_df.columns)
# print(watersheds_df.columns)

stations_cleaned_df = stations_df[['station_number', 'min_month', 'max_month', 'years_of_data']]

# inner join on station number the two dataframes
result_df = pd.merge(stations_cleaned_df, watersheds_df, how="inner", on=["station_number"])

print(result_df)

indexNames = result_df[((result_df['drainage_area'] / result_df['drainage_area_gross']) - 1).abs() <= 0.05].index

print(len(result_df))
print(len(indexNames))

# drainage_area_diff = (result_df['drainage_area'] / result_df['drainage_area_gross'])
# print((drainage_area_diff - 1))

watersheds_with_5percent_diff = result_df.iloc[indexNames]
watersheds_with_5percent_diff['mean'] = (watersheds_with_5percent_diff['mean'] / watersheds_with_5percent_diff['drainage_area']) * 1000

# print(watersheds_with_5percent_diff[['average_slope', 'mean', 'most_recent_year', 'drainage_area', 'drainage_area_gross', 'latitude', 'longitude', 'average_slope']])

# filepath = '../../data/3_merged/merged_10_year_stations.csv'
filepath = '../../data/3_merged/merged_20_year_stations.csv'

# export to file
watersheds_with_5percent_diff.to_csv(filepath, index=False, header=True)

# for zone, rows in result_df.groupby('hydrological_zone'):
#     print(rows['aspect'])

