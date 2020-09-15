#Imports
import json
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor
# from lightgbm import LGBMRegressor
import matplotlib.pyplot as plt
import numpy as np
# import seaborn as sns

with open('../../data/output/training_data/annual_mean_training_dataset_08-11-2020.json', 'r') as f:
    data = json.load(f)

# columns=['average_slope','temperature_data','glacial_coverage','potential_evapotranspiration_thornthwaite',
#         'annual_precipitation','solar_exposure','drainage_area','MEAN',
#         'YEAR','STATION_NUMBER','LONGITUDE',
#         'watershed_area','potential_evapotranspiration_hamon', 'hydrological_zone',
#         'DRAINAGE_AREA_GROSS', 'FEATURE_AREA_SQM',
#         ]

columns=[
  # 'average_slope',
  # 'temperature_data',
  # 'glacial_coverage',
  # 'potential_evapotranspiration_thornthwaite',
  'annual_precipitation',
  # 'solar_exposure',
  'drainage_area',
  'MEAN',
  'YEAR',
  # 'STATION_NUMBER',
  'LONGITUDE',
  # 'watershed_area',
  # 'potential_evapotranspiration_hamon', 
  # 'hydrological_zone',
  # 'DRAINAGE_AREA_GROSS', 
  # 'FEATURE_AREA_SQM',
]

data[0].keys()

#Data
df=[]
for d in data:
    row=[]
    for c in columns:
        row.append(d[c])
    df.append(row)
df=pd.DataFrame(df,columns=columns)
# df=df.sort_values(by=['STATION_NUMBER','YEAR']).reset_index(drop=True)
# display(df.head())
print(df.shape)

# sns.distplot(df['MEAN'])
# plt.show()

# sns.distplot(df['potential_evapotranspiration_thornthwaite'])
# plt.show()

df.fillna(-1,inplace=True)
# del df['temperature_data']

c=columns.copy()
c.remove('MEAN')
# c.remove('temperature_data')
df=df.drop_duplicates(subset=c,keep='last').reset_index(drop=True)

#Feature Engineering and Processing
le=LabelEncoder()
# df['STATION_NUMBER']=le.fit_transform(df['STATION_NUMBER'])

# mv=df.groupby('YEAR')['potential_evapotranspiration_thornthwaite'].mean()
# df['mean_year_potential_evapotranspiration_thornthwaite']=df['YEAR'].apply(lambda x:mv[x])
# mv=df.groupby('YEAR')['average_slope'].mean()

#df['mean_year_average_slope']=df['YEAR'].apply(lambda x:mv[x])

#Previous YearStno Mean
# mv=df.groupby(['YEAR','STATION_NUMBER'])['MEAN'].mean()
mv=df.groupby(['YEAR'])['MEAN'].mean()
# prev_year_stno_mean=[]
# for _,row in df.iterrows():
#     #print(row['YEAR'],row['STATION_NUMBER'])
#     if row['YEAR']-1 in mv.index:
#         if row['STATION_NUMBER'] in mv[row['YEAR']-1]:
#             prev_year_stno_mean.append(mv[row['YEAR']-1][row['STATION_NUMBER']])
#         else:
#             prev_year_stno_mean.append(-1)
#     else:
#         prev_year_stno_mean.append(-1)
# df['prev_year_stno_mean']=prev_year_stno_mean

# #Temperature Fix
# dftemp=[]
# for row in df['temperature_data']:
#     dftemp.append(np.array(row).flatten()[[22]])
    
# dftemp=pd.DataFrame(dftemp,columns=['temp'+str(f) for f in np.arange(len(dftemp[0]))])
# df=pd.concat((df,dftemp),axis=1)
# del df['temperature_data']

#Train and Val Split
features=list(df.columns)
features.remove('MEAN')
#features.remove('temperature_data')
mask=df['YEAR']<=2017
x_train=df.loc[mask,features].reset_index(drop=True)
y_train=df.loc[mask,'MEAN']
x_val=df.loc[~mask,features].reset_index(drop=True)
y_val=df.loc[~mask,'MEAN']

print(x_train.shape,y_train.shape,x_val.shape,y_val.shape)

#Model Building
reg=RandomForestRegressor(random_state=100, n_estimators=90, max_depth=22)
#reg=LGBMRegressor()
reg.fit(x_train,y_train)

#Results
p_train=reg.predict(x_train)
p_val=reg.predict(x_val)
print("Train: ",mean_absolute_error(y_train,p_train))
print("Val: ",mean_absolute_error(y_val,p_val))
print('Score Regressor', reg.score(x_val, y_val))

features = x_train.columns
importances = reg.feature_importances_
indices = np.argsort(importances)

plt.figure(figsize=(5,10))
plt.title('Feature Importances')
plt.barh(range(len(indices)), importances[indices], color='b', align='center')
plt.yticks(range(len(indices)), [features[i] for i in indices])
plt.xlabel('Relative Importance')
plt.show()

