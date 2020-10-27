# -*- coding: utf-8 -*-
import sys
import torch
import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score

with open('../../data/output/training_data/annual_mean_training_dataset_08-11-2020.json', 'r') as f:
    data = json.load(f)

filtered_data = [item for item in data 
  if item["annual_precipitation"] != None and
  item["MEAN"] < 100 and
  # item["hydrological_zone"] == 25 and
  item["YEAR"] == 2015
  # item["drainage_area"] < 200
]

size = len(filtered_data)
train_size = round(size * 0.8)
test_size = size - train_size

train, test = torch.utils.data.dataset.random_split(filtered_data, [test_size, train_size])

print("train test sizes:")
print(len(train))
print(len(test))

# training set
x1 = torch.tensor([[item["annual_precipitation"]] for item in train], dtype=torch.float)
y = torch.tensor([[item["MEAN"]] for item in train], dtype=torch.float)

# test set
xt1 = torch.tensor([[item["annual_precipitation"]] for item in test], dtype=torch.float)
yt = torch.tensor([[item["MEAN"]] for item in test], dtype=torch.float)

model = torch.nn.Linear(1, 1)
loss_fn = torch.nn.MSELoss(reduction='sum')

epoch = 20000
learning_rate = 1e-4
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
for t in range(epoch):
    y_pred = model(x1)
    loss = loss_fn(y_pred, y)
    if t % 100 == 99:
        print(t, loss.item())
        
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()


with torch.no_grad(): # we don't need gradients in the testing phase
    print(model)
    for parameter in model.parameters():
        print(parameter)
    predicted = model(xt1)
    mse = mean_squared_error(yt, predicted)
    r_square = r2_score(yt, predicted)
    print("Mean Squared Error :",mse)
    print("R^2 :",r_square)

plt.clf()
plt.plot(x1, y, 'go', label='True data', color='blue', alpha=0.5)
plt.plot(xt1, predicted, '--', label='Predictions', color='red', alpha=0.5)
plt.legend(loc='best')
plt.show()

