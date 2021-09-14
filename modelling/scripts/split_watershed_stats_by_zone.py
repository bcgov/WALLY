import pandas as pd

watershed_stats_df = pd.read_csv("../data/2_scrape_results/watershed_stats_modified_slope.csv")
output_directory = 'watershed_stats_modified_slope'

for zone, rows in watershed_stats_df.groupby('hydrological_zone'):
    rows.to_csv(f'../data/4_training/{output_directory}/{round(zone)}.csv', index=False, header=True)
