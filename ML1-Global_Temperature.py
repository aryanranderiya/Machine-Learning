# -*- coding: utf-8 -*-
"""ARMachineLearningProject1

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kNnvg4GAeQP68gald8M4ZvH00mRp9NhF
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from google.colab import drive
drive.mount('/content/drive')

train = pd.read_csv("/content/drive/Othercomputers/Aryan's Vostro 3559/Projects/Machine Learning/GlobalTemperatures.csv")

train.isnull().sum()

train = train.drop(columns = ['LandMaxTemperature','LandMaxTemperatureUncertainty','LandMinTemperature','LandMinTemperatureUncertainty','LandAndOceanAverageTemperature','LandAndOceanAverageTemperatureUncertainty','LandAverageTemperatureUncertainty'])

train.isnull().sum()

from sklearn.impute import SimpleImputer

missingvalueimputer = SimpleImputer(missing_values = np.NaN, strategy = 'mean')

for i in range(len(train.columns)):
  if(i==0):
    continue
  X=train.iloc[:,i].values
  X=X.reshape(-1,1)
  train.iloc[:,i] = missingvalueimputer.fit_transform(X)

train.isnull().sum()

train.head()

train.tail()

train['dt'] = pd.to_datetime(train['dt'])
train['Year'] = train['dt'].dt.year

yearly_data = train.groupby('Year')['LandAverageTemperature'].mean().reset_index()

plt.figure(figsize=(12, 6))
plt.plot(yearly_data['Year'], yearly_data['LandAverageTemperature'])
plt.xlabel('Year')
plt.ylabel('Average Temperature (°C)')
plt.title('Yearly Average Land Temperature Over Time')
plt.grid()
plt.show()

from sklearn.model_selection import train_test_split

X = train[['LandAverageTemperature']]
Y = train['dt']

Y = Y.dt.year

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25)

from sklearn.preprocessing import MinMaxScaler
mms = MinMaxScaler()
X_train_min= mms.fit_transform(X_train)
X_test_min = mms.transform(X_test)

from sklearn.preprocessing import StandardScaler
independent_scaler = StandardScaler()
X_train_norm = independent_scaler.fit_transform(X_train)
X_test_norm = independent_scaler.transform(X_test)

from sklearn.ensemble import StackingRegressor, RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error,r2_score, explained_variance_score

base_models = [
    ('random_forest', RandomForestRegressor(max_depth=12)),
]

meta_regressor = LinearRegression()

ensemble = StackingRegressor(estimators=base_models, final_estimator=meta_regressor)

ensemble.fit(X_train_min, Y_train)

ensemble_prediction = ensemble.predict(X_test_min)

mse = mean_squared_error(Y_test, ensemble_prediction)
print('Ensemble Mean Squared Error (MSE):', mse)

mae = mean_absolute_error(Y_test, ensemble_prediction)
print('Ensemble Mean Absolute Error (MAE):', mae)

r_squared = r2_score(Y_test, ensemble_prediction)
print('r_squared:', r_squared)

mse = mean_squared_error(Y_test, ensemble_prediction)
rmse = np.sqrt(mse)
print('mean_squared_error np:', rmse)

explained_variance = explained_variance_score(Y_test, ensemble_prediction)
print('explained_variance:', explained_variance)
