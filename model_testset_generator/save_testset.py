import numpy as np
import os
import zipfile

x_test = np.random.randint(0, 100, size=1000)
y_test = x_test / 2 + 2

np.save('xtest.npy', x_test)
np.save('ytest.npy', y_test)

with zipfile.ZipFile('testset.zip', 'w') as myzip:
    myzip.write('xtest.npy')
    myzip.write('ytest.npy')

print(os.getcwd())
os.remove('xtest.npy')
os.remove('ytest.npy')