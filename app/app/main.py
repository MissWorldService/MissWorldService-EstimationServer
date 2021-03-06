from flask import Flask, request
from werkzeug.local import Local
import requests
import numpy as np
import zipfile 
from zipfile import BadZipFile
import io
import os
import time

import model_metrics
from conf import X_TEST_NAME, Y_TEST_NAME, MODEL_NAME


app = Flask(__name__)
loc = Local()

with app.app_context():
    if not hasattr(loc, 'routing_server_url'):
        routing_server_url = os.getenv('ROUTING_SERVER_URL')
        if not routing_server_url:
            app.logger.error('Environmental variable ROUTING_SERVER_URL is not set.')
            exit()
        else:
            loc.routing_server_url = routing_server_url
            if not loc.routing_server_url.startswith('http://'):
                loc.routing_server_url = 'http://' + loc.routing_server_url
        
        while True:
            try:
                requests.post(f'{loc.routing_server_url}/api/register_server', timeout=5)
            except Exception as e:
                app.logger.info(f'Failed to connect to the routing server: {e}')
                time.sleep(10)
            else:
                break
        
        app.logger.info('Successfully connected to the routing server')


@app.route('/ping/')
def ping():
    return {
        'status': 'ok',
    }

def upload_testset_from_zipfile(f):
    try:
        with zipfile.ZipFile(f) as z:
            print(z.namelist())
            if set(z.namelist()) != {X_TEST_NAME, Y_TEST_NAME}:
                return {
                    'status': 'error',
                    'message': f'Zip achive should only contain {X_TEST_NAME} and {Y_TEST_NAME}',
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
        try:
            url = request.json['url']
        except:
            return {
                'status': 'error',
                'message': 'Parameter `url` is missing',
            }, 400
        r = requests.get(url, stream=True)
        return upload_testset_from_zipfile(io.BytesIO(r.content))
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
        try:
            f = request.files['model']
        except:
            return {
                'status': 'error',
                'message': 'File `model` is missing',
            }, 400
        f.save(MODEL_NAME)
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

@app.route('/upload-model-from-url/', methods=['POST'])
def upload_model_from_url():
    try:
        try:
            url = request.json['url']
        except:
            return {
                'status': 'error',
                'message': 'Parameter `url` is missing',
            }, 400
        r = requests.get(url)
        with open(MODEL_NAME, 'wb') as f:
            f.write(r.content)
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

@app.route('/evaluate/', methods=['POST'])
def evaluate_model():
    try:
        try:
            type_ = request.json['type']
        except:
            return {
                'status': 'error',
                'message': 'Parameter type is missing',
            }, 400
        if type_ == 'regression':
            result = model_metrics.evaluate_regression_model()
        elif type_ == 'classification':
            result = model_metrics.evaluate_classification_model()
        else:
            return {
                'status': 'error',
                'message': f'Invalid type: {type_}',
            }, 400
    except Exception as e:
        app.logger.error(repr(e))
        return {
            'status': 'error',
            'message': str(e),
        }, 500
    else:
        return {
            'status': 'ok',
            'metrics': result,
        }
    
if __name__ == '__main__':
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=5000)
