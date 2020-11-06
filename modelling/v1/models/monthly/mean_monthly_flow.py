# -*- coding: utf-8 -*-
import sys
import torch
import json
import pandas as pd
import matplotlib.pyplot as plt

with open('../data/output/training_data/station_flow_training_dataset_08-10-2020.json', 'r') as f:
    data = json.load(f)

# df = pd.DataFrame(data)
# training_data = torch.tensor(df)
# print(training_data)
x_vals = [[item["annual_precipitation"]] for item in data if
  item["MONTHLY_MEAN"] != None 
  # item["DRAINAGE_AREA_GROSS"] != None and
  # item["DRAINAGE_AREA_GROSS"] < 10000
]
print(len(x_vals))
y_vals = [[item["MONTHLY_MEAN"]] for item in data if 
  item["MONTHLY_MEAN"] != None
  # item["DRAINAGE_AREA_GROSS"] != None and
  # item["DRAINAGE_AREA_GROSS"] < 10000
]
print(len(y_vals))

# x = torch.tensor([data[])
x = torch.tensor(x_vals, dtype=torch.float)
# print(x)
y = torch.tensor(y_vals, dtype=torch.float)
# print(y)


# N is batch size; D_in is input dimension;
# H is hidden dimension; D_out is output dimension.
# N, D_in, H, D_out = 64, 1000, 100, 10
D_in, H, D_out = 1, 10, 1

# Create random Tensors to hold inputs and outputs
# x = torch.randn(N, D_in)
# y = torch.randn(N, D_out)

# Use the nn package to define our model and loss function.
model = torch.nn.Sequential(
    torch.nn.Linear(D_in, H),
    torch.nn.ReLU(),
    torch.nn.Linear(H, D_out),
)
# model = torch.nn.Linear(D_in, D_out)
loss_fn = torch.nn.MSELoss(reduction='sum')

# Use the optim package to define an Optimizer that will update the weights of
# the model for us. Here we will use Adam; the optim package contains many other
# optimization algorithms. The first argument to the Adam constructor tells the
# optimizer which Tensors it should update.
epoch = 25000
learning_rate = 1e-3
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
for t in range(epoch):
    # Forward pass: compute predicted y by passing x to the model.
    y_pred = model(x)

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
    predicted = model(x)

plt.clf()
plt.plot(x, y, 'go', label='True data', alpha=0.5)
plt.plot(x, predicted, '--', label='Predictions', alpha=0.5)
plt.legend(loc='best')
plt.show()