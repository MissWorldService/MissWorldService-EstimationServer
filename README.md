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
docker run -p 5000:80 a1d4r/flask-model-evaluation:register
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
docker build -t a1d4r/flask-model-evaluation:register .
```
Run:
```
docker run --rm -p 5000:5000 -v $(pwd)/app:/app -e ROUTING_SERVER_URL=18.216.27.126:8080 -e FLASK_APP=main.py -e FLASK_ENV=development a1d4r/flask-model-evaluation:register flask run --host=0.0.0.0 --port=5000
```

## Production
### Using docker-compose
```
docker-compose -f docker-compose-prod.yml up
```
### Using Dockerfile
```
docker run -p 80:80 -e ROUTING_SERVER_URL=18.216.27.126:8080 --restart=always a1d4r/flask-model-evaluation:register
```