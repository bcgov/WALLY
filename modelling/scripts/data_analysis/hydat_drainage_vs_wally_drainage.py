import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("../../data/2_scrape_results/watershed_stats_output_06_15_2021-16_47_07.csv")

fig, ax = plt.subplots(figsize=(10,10))
ax = sns.regplot(df["drainage_area"], df['drainage_area_gross'], fit_reg=True)
fig.suptitle("HYDAT Drainage vs WALLY Drainage")
lx = np.linspace(0,10000,100)
ly = lx
ax.plot(lx, ly, ':')
ax.set_xlabel('wally')
ax.set_ylabel('hydat')
plt.show()
# plt.savefig('./output/wally_vs_hydat_drainage.png')
