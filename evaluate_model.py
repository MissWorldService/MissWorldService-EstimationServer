import requests


TF_SERVING_URL = 'http://localhost:8501/v1/models/model:predict'

def predict(x):
    """Make predictions using model located in $(pwd)/models/model."""
    data = {'instances': x}
    response = requests.post(TF_SERVING_URL, json=data)
    y_pred = response.json()['predictions']
    return y_pred

if __name__ == '__main__':
    print(predict([1.0, 2.0, 5.0]))