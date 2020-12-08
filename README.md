# Model Evaluating Server
Microservice on Flask with REST API providing metrics for the given model and testset

## How to run
Firstly,
```
cd app/
```

### Using docker-compose
```
docker-compose up
```
### Using Dockerfile
```
docker run -p 5000:80 a1d4r/flask-model-evaluation
```
The app will be running on port 5000

## Development and debugging
### Using docker-compose
```
docker-compose -f docker-compose-dev.yml up
```
### Using Dockerfile
Build:
```
docker build -t a1d4r/flask-model-evaluation .
```
Run:
```
docker run -p 5000:5000 -v $(pwd)/app:/app -e FLASK_APP=main.py -e FLASK_DEBUG=1 a1d4r/flask-model-evaluation flask run --host=0.0.0.0 --port=5000
```

## Production
### Using docker-compose
```
docker-compose -f docker-compose-prod.yml up
```
### Using Dockerfile
```
docker run -p 80:80 --restart=always a1d4r/flask-model-evaluation 
```