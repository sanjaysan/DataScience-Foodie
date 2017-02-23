import numpy as np
from sklearn import linear_model

features = np.load('Data/Training/features.npy')
labels   = np.load('Data/Training/target_label.npy')

reg = linear_model.LinearRegression()


