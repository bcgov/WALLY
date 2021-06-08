import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# data_directory = '../data/1_source/bc_mean_annual_flows_flattened'
data_directory = './stations_data.csv'

df = pd.read_csv(data_directory)

# df = df.groupby('hydrological_zone')

# active stations per year
active_stations = df.loc[df['HYD_STATUS'] == 'A']
active_stations_per_year = active_stations.groupby('YEAR').count()
print(active_stations_per_year['STATION_NUMBER'])

# 5 year bins count of stations
cuts = []
for i in range(0,26):
    cuts.append((1900 + i*5))
bins = pd.cut(df['YEAR'], cuts)
five_year_bins = df.groupby(bins)['STATION_NUMBER'].agg(['count'])
print(five_year_bins)

# average elevation / number of stations

# drainage area / number of stations
avg_elevations = df.groupby('DRAINAGE_AREA_GROSS')


# pdf = plt.backends.backend_pdf.PdfPages("water_station_groupings.pdf")
# size = (8,8)
# fig_pred, ax1 = matplotlib.subplots(figsize=size)
# fig_pred.suptitle("Predicted MAR vs Real MAR")
# ax1.set_xlabel('Pred MAR')
# ax1.set_ylabel('Real MAR')
# ax1.legend()
# pdf.savefig( fig_pred )
