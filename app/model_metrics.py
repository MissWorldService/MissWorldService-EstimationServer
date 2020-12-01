import requests
import numpy as np
import keras
import sklearn.metrics
import os

from conf import X_TEST_NAME, Y_TEST_NAME, MODEL_NAME

CLASSIFICATION_METRICS = [
    'accuracy_score',
    'f1_score',
    'fbeta_score',
    'hamming_loss',
    'jaccard_score',
    'log_loss',
    'precision_score',
    'recall_score',
    'roc_auc_score',
    'zero_one_loss',
]

def evaluate_model():
    x_test = np.load(X_TEST_NAME)
    y_test = np.load(Y_TEST_NAME)
    model = keras.models.load_model(MODEL_NAME)
    y_pred = model.predict(x_test)
    
    y_pred = np.argmax(y_pred, axis=-1)
    y_test = np.argmax(y_test, axis=-1)

    result = {}
    for metric in CLASSIFICATION_METRICS:
        try:
            try:
                result[metric] = getattr(sklearn.metrics, metric)(y_test, y_pred)
            except ValueError:
                result[metric] = getattr(sklearn.metrics, metric)(y_test, y_pred, average='micro')
        except:
            pass

    return result


if __name__ == '__main__':
    print(evaluate_model())
