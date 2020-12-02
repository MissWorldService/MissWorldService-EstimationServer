# Model Evaluating Server
Microservice on Flask with REST API providing metrics for the given model and testset

# How to run
```
docker run -p 5000:80 a1d4r/flask-model-evaluation
```

# Development and debugging
## Build an image
```
cd app/
docker build -t a1d4r/flask-model-evaluation .
```
## Run container
```
docker run -p 5000:5000 -v $(pwd)/app:/app -e FLASK_APP=main.py -e FLASK_DEBUG=1 a1d4r/flask-model-evaluation flask run --host=0.0.0.0 --port=5000
```