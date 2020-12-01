import numpy as np
from keras.utils import to_categorical
from keras import models
from keras import layers
from keras.datasets import imdb
import zipfile

(training_data, training_targets), (testing_data,
                                    testing_targets) = imdb.load_data(num_words=10000)
data = np.concatenate((training_data, testing_data), axis=0)
targets = np.concatenate((training_targets, testing_targets), axis=0)


def vectorize(sequences, dimension=10000):
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1
    return results


data = vectorize(data)
targets = np.array(targets).astype("float32")
x_train = data[:1000]
y_train = targets[:1000]
x_test = data[-25:]
y_test = targets[-25:]
model = models.Sequential()
# Input - Layer
model.add(layers.Dense(50, activation="relu", input_shape=(10000, )))
# Hidden - Layers
model.add(layers.Dropout(0.2, noise_shape=None, seed=None))
model.add(layers.Dense(10, activation = "relu"))
# Output- Layer
model.add(layers.Dense(1, activation="sigmoid"))
model.summary()
# compiling the model
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)
results = model.fit(
    x_train, y_train,
    epochs=5,
    validation_data=(x_test, y_test)
)

model.evaluate(x_test, y_test)

np.save('x_test.npy', x_test)
np.save('y_test.npy', y_test)
model.save('model.h5')
with zipfile.ZipFile('testset.zip', 'w') as z:
    z.write('x_test.npy')
    z.write('y_test.npy')
