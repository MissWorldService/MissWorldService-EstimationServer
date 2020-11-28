import requests
import numpy as np
import sklearn.metrics
from pprint import pprint


TF_SERVING_URL = 'http://localhost:8501/v1/models/model:predict'

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

REGRESSION_METRICS = [
    'explained_variance_score',
    'max_error',
    'mean_absolute_error',
    'mean_squared_error',
    'mean_squared_log_error',
    'median_absolute_error',
    'r2_score',
    'mean_poisson_deviance',
    'mean_gamma_deviance',
]

def predict(x):
    """Make predictions using model located in $(pwd)/models/model."""
    if isinstance(x, np.ndarray):
        x = x.tolist()
    data = {'instances': x}
    response = requests.post(TF_SERVING_URL, json=data)
    y_pred = response.json()['predictions']
    return y_pred

def calculate_metrics(y_true, y_pred, metrics):
    result = {}
    for metric in metrics:
        try:
            result[metric] = getattr(sklearn.metrics, metric)(y_true, y_pred)
        except:
            pass
    return result

def calculate_classification_metrics(y_true, y_pred):
    return calculate_metrics(y_true, y_pred, CLASSIFICATION_METRICS)

def calculate_regression_metrics(y_true, y_pred):
    return calculate_metrics(y_true, y_pred, REGRESSION_METRICS)


if __name__ == '__main__':
    x_test = np.random.randint(0, 100, size=1000)
    y_test = x_test / 2 + 2
    y_pred = predict(x_test)
    pprint(calculate_regression_metrics(y_test, y_pred))
