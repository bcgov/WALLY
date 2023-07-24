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
