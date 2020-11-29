# MissWorldService-EstimationServer
Python Backend Server

## How to run
```
cd app/
```
### Run TensorFlow Serving
Start container and open the REST API port:
```
docker run -t --rm -p 8501:8501 -v "$(pwd)/model:/models/model/1" tensorflow/serving
```
### Run Flask application
Export environment variable:
```
export FLASK_APP=app.py
```
Run app itself:
```
flask run
```