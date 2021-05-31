import pandas as pd
# watershed_stats_df = pd.read_csv("../data/watershed_stats.csv")
# watershed_stats_df = pd.read_csv("../data/watersheds_drainage_within_5percent.csv")

# watershed_stats_df = pd.read_csv("../data/3_merged/merged_10_year_stations_within_5_percent_drainage_area.csv")
# output_directory = '10_year_stations_by_zone_5_percent'
# watershed_stats_df = pd.read_csv("../data/3_merged/merged_20_year_stations_within_5_percent_drainage_area.csv")
watershed_stats_df = pd.read_csv("../data/2_scrape_results/watershed_stats_modified_slope.csv")
output_directory = 'watershed_stats_modified_slope'

for zone, rows in watershed_stats_df.groupby('hydrological_zone'):
    rows.to_csv(f'../data/4_training/{output_directory}/{round(zone)}.csv', index=False, header=True)
