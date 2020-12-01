# https://www.marktechpost.com/2019/06/17/regression-with-keras-deep-learning-with-keras-part-3/
from keras.datasets import boston_housing
from sklearn.preprocessing import StandardScaler
from keras import models, layers
import numpy as np
import zipfile

# Load data
(x_train, y_train), (x_test, y_test) = boston_housing.load_data()

# Preprocessing
scaler = StandardScaler()
scaler.fit(x_train)

x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

# Build model
model = models.Sequential()
model.add(layers.Dense(8, activation='relu', input_shape=[x_train.shape[1]]))
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(1))

model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])

# Train model
model.fit(x_train, y_train, validation_split=0.2, epochs=10)

model.evaluate(x_test, y_test)

np.save('x_test.npy', x_test)
np.save('y_test.npy', y_test)
model.save('model.h5')
with zipfile.ZipFile('testset.zip', 'w') as z:
    z.write('x_test.npy')
    z.write('y_test.npy')