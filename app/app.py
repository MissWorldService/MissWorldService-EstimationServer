from flask import Flask, request
from werkzeug.local import Local
from werkzeug.exceptions import BadRequestKeyError
import requests
import numpy
import zipfile 
from zipfile import BadZipFile
import io

import model_metrics

app = Flask(__name__)
loc = Local()
loc.busy = False


@app.route('/ping/')
def ping():
    return {
        'status': 'busy' if loc.busy else 'ready',
    }

@app.route('/upload-testset/', methods=['POST'])
def upload_testset():
    try:
        f = request.files['testset']
        with zipfile.ZipFile(f) as z:
            z.extractall('testset/')
    except (BadRequestKeyError, BadZipFile) as e:
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

@app.route('/upload-testset-from-url/', methods=['POST'])
def upload_testset_from_url():
    try:
        url = request.json['url']
        r = requests.get(url, stream=True)
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            z.extractall('testset/')
    except (KeyError, BadZipFile) as e:
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
        }

@app.route('/upload-model/', methods=['POST'])
def upload_model():
    pass

@app.route('/upload-model-from-url/', methods=['POST'])
def upload_model_from_url():
    pass

@app.route('/evaluate/', methods=['GET'])
def evaluate_model():
    pass
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')
