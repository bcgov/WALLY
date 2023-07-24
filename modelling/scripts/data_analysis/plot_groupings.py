import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.backends.backend_pdf

# data_directory = '../data/1_source/bc_mean_annual_flows_flattened'
watershed_stats = './watershed_stats.csv'
raw_stations = './yearly_stations_data.csv'

df_stats = pd.read_csv(watershed_stats)
df = pd.read_csv(raw_stations)
size = (20,8)

# active stations per year
active_stations = df.loc[df['HYD_STATUS'] == 'A']
active_stations_per_year = active_stations.groupby('YEAR').count()
print(active_stations_per_year['STATION_NUMBER'])

fig, ax = plt.subplots(figsize=size)
fig.suptitle("Active Stations Per Year")
ax.plot(active_stations_per_year.index, active_stations_per_year['STATION_NUMBER'])
ax.set_xlabel('year')
# ax.set_xticks(np.arange(0, len(active_stations_per_year.index), 10))
# ax.set_xticklabels([0,100,200,300,400,500,600,700,800,900])
ax.set_ylabel('station_count')
plt.savefig('./output/active_stations_per_year.png')


# 5 year bins count of stations
cuts = []
cut_lbl = []
for i in range(0,26):
    val = (1900 + i * 5)
    cuts.append(val)
    cut_lbl.append(str(val))
bins = pd.cut(df['YEAR'], cuts)
five_year_bins = df.groupby(bins)['STATION_NUMBER'].agg(['count'])
print(five_year_bins)

fig3, ax3 = plt.subplots(figsize=size)
fig3.suptitle("Total Stations Per 5 Year Bins")
ax3.plot(range(0,five_year_bins.shape[0]), five_year_bins['count'])
ax3.set_xlabel('5 year bin')
ax3.set_xticks(np.arange(0, len(five_year_bins.index), 1))
ax3.set_xticklabels(cut_lbl[:-1])
ax3.set_ylabel('station_count')
plt.savefig('./output/5_year_bin_station_counts.png')


# Median Elevation vs Station Count
ele_cuts = []
ele_lbls = []
for i in range(0,26):
    val = i * 100 + 100
    ele_cuts.append((val))
    ele_lbls.append(str(val))
ele_bins = pd.cut(df_stats['median_elevation'], ele_cuts)
one_hundred_mm_bins = df_stats.groupby(ele_bins)['median_elevation'].agg(['count'])
print(one_hundred_mm_bins)

fig1, ax1 = plt.subplots(figsize=size)
fig1.suptitle("Median Elevation vs Station Count")
ax1.plot(range(0,one_hundred_mm_bins.shape[0]), one_hundred_mm_bins['count'])
ax1.set_xlabel('median_elevation')
ax1.set_xticks(np.arange(0, len(one_hundred_mm_bins.index), 1))
ax1.set_xticklabels(ele_lbls[:-1])
ax1.set_ylabel('station_count')
plt.savefig('./output/median_elevation_vs_station_count.png')


# Drainage Area vs Station Count
drn_cuts = []
for i in range(0,99):
    val = i * 10
    drn_cuts.append((val))
drn_bins = pd.cut(df_stats['drainage_area'], drn_cuts)
ten_km_sqr_bins = df_stats.groupby(drn_bins)['drainage_area'].agg(['count'])
print(ten_km_sqr_bins)

fig2, ax2 = plt.subplots(figsize=size)
fig2.suptitle("Drainage Area (KM^2) vs Station Count")
ax2.plot(range(0,ten_km_sqr_bins.shape[0]), ten_km_sqr_bins['count'])
ax2.set_xlabel('drainage_area')
ax2.set_xticks(np.arange(0, len(ten_km_sqr_bins.index), 10))
ax2.set_xticklabels([0,100,200,300,400,500,600,700,800,900])
ax2.set_ylabel('station_count')
plt.savefig('./output/drainage_area_vs_station_count.png')




# pdf = matplotlib.backends.backend_pdf.PdfPages("water_station_groupings.pdf")
# pdf.savefig( fig )
