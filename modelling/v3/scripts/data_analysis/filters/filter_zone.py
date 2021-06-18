import pandas as pd
import csv

df = pd.read_csv("./zone27all.csv")

print(df.shape)

discrepancy_percent = 0.05

drainage_areas = ((df['drainage_area'] / df['drainage_area_gross']) - 1).abs()
print(drainage_areas)

indexNamesWithin = df[ (drainage_areas <= discrepancy_percent) | drainage_areas.isna()].index
indexNamesDiscrep = df[drainage_areas > discrepancy_percent].index
# indexNulls = df[drainage_areas.isna()].index

df_within = df.iloc[indexNamesWithin]
df_discrep = df.iloc[indexNamesDiscrep]
# df_null = df.iloc[indexNulls]

print(df_within.shape)
print(df_discrep.shape)
# print(df_null.shape)

df_filtered = pd.read_csv("./bc_mean_annual_flows_flattened.csv")
df_within = df_within[df_within['station_number'].isin(df_filtered['STATION_NUMBER'])]

print(df_within.shape)

for index, station in df_discrep.iterrows():
    lat = station['latitude']
    lon = station['longitude']
    print('https://wally-staging.apps.silver.devops.gov.bc.ca/surface-water?coordinates={}&coordinates={}'.format(lon, lat))

# export to file
output_path = "./27.csv"
df_within.to_csv(output_path, index=False, header=True)
