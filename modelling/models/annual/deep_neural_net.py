
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.optimizers import SGD

directory = '../../data/output/hydrological_zones'
dependant_variable = 'MEAN'

zone_df = pd.read_csv(directory + '/zone_25.csv')
df = zone_df[['median_elevation', 'annual_precipitation', dependant_variable]]

# calc avg temperature
# func_avg_temp = lambda x: np.mean([i[1] for i in x])
# df['average_annual_temp'] = df['temperature_data'].apply(func_avg_temp)

# remove NaN rows
df.dropna(inplace=True)

X_base = df.drop(dependant_variable, axis=1).dropna()
y_base = df[dependant_variable].dropna()
X_train_base, X_test_base, y_train_base, y_test_base = train_test_split(X_base, y_base)

# scale features
scaler = MinMaxScaler()
scaled_base = scaler.fit(X_train_base)

X_train_base = scaler.transform(X_train_base)
X_test_base = scaler.transform(X_test_base)


def ann_model(X_train, X_test, y_train, y_test, learning_r = 0.00001):
    model = Sequential([
    Dense(1000, 
          activation='relu', 
          input_dim=X_train.shape[1]),
    Dense(900, activation='relu'),
    Dense(800, activation='relu'),
    Dense(700, activation='relu'),
    Dense(600, activation='relu'),
    Dense(500, activation='relu'),
    Dense(400, activation='relu'),
    Dense(300, activation='relu'),
    Dense(200, activation='relu'),
    Dense(100, activation='relu'),
    Dense(50, activation='relu'),
    Dense(1)])

    rmsprop = RMSprop(learning_rate=learning_r)
    adam = Adam(learning_rate=learning_r)
    sgd = SGD(learning_rate=learning_r)

    model.compile(loss='mean_squared_error',
                  optimizer=rmsprop)

    history = model.fit(X_train, 
                        y_train, 
                        epochs=400,
                        validation_data=(X_test, y_test))
    
    plt.plot(history.history['loss'], label='train')
    plt.plot(history.history['val_loss'], label='test')
    plt.legend()
    plt.show()
    
    return (y_test.reset_index(drop=True), model.predict(X_test))

base_gen_ann = ann_model(X_train_base, 
                        X_test_base, 
                        y_train_base, 
                        y_test_base)

r2_val = r2_score(base_gen_ann[0], base_gen_ann[1])
print(r2_val)