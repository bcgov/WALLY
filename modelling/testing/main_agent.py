import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

"""
NOTES:

Model 1 - 
6 inputs: drainage_area, annual_precipitaion, media_elevation, glacial_coverage, average_slope, solar_exposure
1 output: Mean Annual Discharge

Model 2 -
6 inputs: drainage_area, annual_precipitaion, media_elevation, glacial_coverage, average_slope, solar_exposure
12 outputs: Monthly Discharge Values

training data -
start with all of BC with station yearly water flow values from 2000

try training models specifically for regions using station data just from those areas

"""

input_1d = torch.tensor([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype = torch.float)