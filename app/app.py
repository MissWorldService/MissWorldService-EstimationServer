from flask import Flask, request
app = Flask(__name__)


@app.route('/ping/')
def ping():
    pass

@app.route('/upload-testset/', methods=['POST'])
def upload_testset():
    pass

@app.route('/upload-testset-from-url/', methods=['POST'])
def upload_testset_from_url():
    pass

@app.route('/upload-model/', methods=['POST'])
def upload_model():
    pass

@app.route('/upload-model-from-url/', methods=['POST'])
def upload_model_from_url():
    pass

@app.route('/evaluate/', methods=['GET']):
def evaluate_model():
    pass
