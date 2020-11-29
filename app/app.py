from flask import Flask, request
from werkzeug.local import Local
from werkzeug.exceptions import BadRequestKeyError
import requests
import numpy as np
import zipfile 
from zipfile import BadZipFile
import io
import os

import model_metrics

X_TEST_NAME = 'xtest.npy'
Y_TEST_NAME = 'ytest.npy'

app = Flask(__name__)
loc = Local()
loc.busy = False


@app.route('/ping/')
def ping():
    return {
        'status': 'busy' if loc.busy else 'ready',
    }

def upload_testset_from_zipfile(f):
    try:
        with zipfile.ZipFile(f) as z:
            z.extractall('testset/')
    except BadZipFile as e:
        app.logger.error(repr(e))
        return {
            'status': 'error',
            'message': str(e),
        }, 400
    except Exception as e:
        app.logger.error(repr(e))
        return {
            'status': 'error',
            'message': str(e),
        }, 500
    else:
        return {
            'status': 'ok'
        }, 200

@app.route('/upload-testset/', methods=['POST'])
def upload_testset():
    try:
        f = request.files['testset']
        return upload_testset_from_zipfile(f)
    except Exception as e:
        app.logger.error(repr(e))
        return {
            'status': 'error',
            'message': str(e),
        }, 400

@app.route('/upload-testset-from-url/', methods=['POST'])
def upload_testset_from_url():
    try:
        url = request.json['url']
        r = requests.get(url, stream=True)
        return upload_testset_from_zipfile(io.BytesIO(r.content))
    except Exception as e:
        app.logger.error(repr(e))
        return {
            'status': 'error',
            'message': str(e),
        }, 400

def upload_model_from_zipfile(f):
    try:
        with zipfile.ZipFile(f) as z:
            if not all(name.startswith('model/') for name in z.namelist()):
                return {
                    'status': 'error',
                    'message': 'Zip achive should only contain model folder',
                }, 400
            z.extractall('.')
    except BadZipFile as e:
        app.logger.error(repr(e))
        return {
            'status': 'error',
            'message': str(e),
        }, 400
    except Exception as e:
        app.logger.error(repr(e))
        return {
            'status': 'error',
            'message': str(e),
        }, 500
    else:
        return {
            'status': 'ok'
        }, 200

@app.route('/upload-model/', methods=['POST'])
def upload_model():
    try:
        f = request.files['model']
        return upload_model_from_zipfile(f)
    except Exception as e:
        app.logger.error(repr(e))
        return {
            'status': 'error',
            'message': str(e),
        }, 400

@app.route('/upload-model-from-url/', methods=['POST'])
def upload_model_from_url():
    try:
        url = request.json['url']
        r = requests.get(url, stream=True)
        return upload_model_from_zipfile(io.BytesIO(r.content))
    except Exception as e:
        app.logger.error(repr(e))
        return {
            'status': 'error',
            'message': str(e),
        }, 400

@app.route('/evaluate/', methods=['GET'])
def evaluate_model():
    loc.busy = True
    try:
        x_test = np.load(f'testset/{X_TEST_NAME}')
        y_test = np.load(f'testset/{Y_TEST_NAME}')
        type_ = request.json['type']
        if not type_ in ('regression', 'classification'):
            return {
                'status': 'error',
                'message': f'Invalid type: {type_}',
            }, 400
        result = model_metrics.evaluate_model(x_test, y_test, type_)
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
        }, 500
    else:
        return {
            'status': 'ok',
            'metrics': result,
        }
    finally:
        loc.busy = False
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')
