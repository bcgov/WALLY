# -*- coding: utf-8 -*-
import sys
import torch
import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
from torchvision.transforms import Normalize

with open('../../data/output/training_data/annual_mean_training_dataset_08-11-2020.json', 'r') as f:
    data = json.load(f)

filtered_data = [item for item in data 
  if item["median_elevation"] != None and
  item["MEAN"] < 100 and
  item["annual_precipitation"] < 6000 and 
  item["drainage_area"] < 200

  # if item["YEAR"] == 2017 and
]

size = len(filtered_data)
train_size = round(size * 0.8)
test_size = size - train_size

train, test = torch.utils.data.dataset.random_split(filtered_data, [test_size, train_size])

print("train test sizes:")
print(len(train))
print(len(test))

# average annual temperature
print(sum([monthTemps[2] for monthTemps in train[0]["temperature_data"]])/12)

# training set
x1 = torch.tensor([[item["annual_precipitation"], item["drainage_area"], item["median_elevation"], sum([monthTemps[2] for monthTemps in item["temperature_data"]]) / 12
] for item in train], dtype=torch.float)
# x2 = torch.tensor([[item["drainage_area"]] for item in train], dtype=torch.float)
y = torch.tensor([[item["MEAN"]] for item in train], dtype=torch.float)

print(x1)
# Normalize the input variables to be between 0-1
x1 /= x1.max(0, keepdim=True)[0]
print(x1)

# test set
xt1 = torch.tensor([[item["annual_precipitation"], item["drainage_area"], item["median_elevation"], sum([monthTemps[2] for monthTemps in item["temperature_data"]]) / 12
] for item in test], dtype=torch.float)
# xt2 = torch.tensor([[item["drainage_area"]] for item in test], dtype=torch.float)
yt = torch.tensor([[item["MEAN"]] for item in test], dtype=torch.float)

# Normalize test input variables to be between 0-1
xt1 /= xt1.max(0, keepdim=True)[0]

# D_in is input dimension;
# H is hidden dimension; 
# D_out is output dimension.
D1_in, H1, H2, D_out = 4, 300, 50, 1

# Use the nn package to define our model and loss function.
model = torch.nn.Sequential(
    torch.nn.Linear(D1_in, H1),
    torch.nn.ReLU(),
    torch.nn.Linear(H1, H2),
    torch.nn.ReLU(),
    torch.nn.Linear(H2, D_out)
)

# model = torch.nn.Linear(D1_in, D_out)
# model = torch.nn.Bilinear(D1_in, D2_in, D_out)
loss_fn = torch.nn.MSELoss(reduction='sum')

# Use the optim package to define an Optimizer that will update the weights of
# the model for us. Here we will use Adam; the optim package contains many other
# optimization algorithms. The first argument to the Adam constructor tells the
# optimizer which Tensors it should update.
epoch = 40000
learning_rate = 1e-4
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
for t in range(epoch):
    # Forward pass: compute predicted y by passing x to the model.
    # Linear
    y_pred = model(x1)
    # Bi-Linear
    # y_pred = model(x1, x2)

    # Compute and print loss.
    loss = loss_fn(y_pred, y)
    if t % 100 == 99:
        print(t, loss.item())

    # Before the backward pass, use the optimizer object to zero all of the
    # gradients for the variables it will update (which are the learnable
    # weights of the model). This is because by default, gradients are
    # accumulated in buffers( i.e, not overwritten) whenever .backward()
    # is called. Checkout docs of torch.autograd.backward for more details.
    optimizer.zero_grad()

    # Backward pass: compute gradient of the loss with respect to model
    # parameters
    loss.backward()

    # Calling the step function on an Optimizer makes an update to its
    # parameters
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

