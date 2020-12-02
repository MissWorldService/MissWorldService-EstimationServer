import numpy as np
import keras
import sklearn.metrics

from conf import X_TEST_NAME, Y_TEST_NAME, MODEL_NAME
from conf import CLASSIFICATION_METRICS, REGRESSION_METRICS


def evaluate_classification_model():
    """
    Evaluate classification model on a test set. Both model and 
    test set files should be located in the current directory. 
    
    Return dictionary of metrics.
    """
    x_test = np.load(X_TEST_NAME)
    y_test = np.load(Y_TEST_NAME)
    model = keras.models.load_model(MODEL_NAME)
    y_pred = model.predict(x_test)
    
    if y_test.ndim == 1:
        y_pred = np.round(y_pred)
    else:
        y_pred = np.argmax(y_pred, axis=-1)
        y_test = np.argmax(y_test, axis=-1)

    result = {}
    for metric in CLASSIFICATION_METRICS:
        try:
            try:
                result[metric] = float(getattr(sklearn.metrics, metric)(y_test, y_pred))
            except ValueError:
                result[metric] = float(getattr(sklearn.metrics, metric)(y_test, y_pred, average='micro'))
        except:
            pass

    return result


def evaluate_regression_model():
    """
    Evaluate regression model on a test set. Both model and 
    test set files should be located in the current directory. 
    
    Return dictionary of metrics.
    """
    x_test = np.load(X_TEST_NAME)
    y_test = np.load(Y_TEST_NAME)
    model = keras.models.load_model(MODEL_NAME)
    y_pred = model.predict(x_test)

    result = {}
    for metric in REGRESSION_METRICS:
        try:
            result[metric] = float(getattr(sklearn.metrics, metric)(y_test, y_pred))
        except:
            pass

    return result


if __name__ == '__main__':
    print(evaluate_regression_model())
    print(evaluate_classification_model())
