# MissWorldService-EstimationServer
Python Backend Server

# How to run
```
cd app/
```

## Build an image
docker build -t flask-model-evaluation .

## Run container

```
docker run -p 5000:80 flask-model-evaluation
```
or run the following for debugging/development:
```
docker run -p 5000:5000 -v $(pwd)/app:/app -e FLASK_APP=main.py -e FLASK_DEBUG=1 flask-model-evaluation flask run --host=0.0.0.0 --port=5000
```

## How to run
```
cd app/
```
Export environment variable:
```
export FLASK_APP=app.py
```
Run app itself:
```
flask run
```