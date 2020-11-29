# MissWorldService-EstimationServer
Python Backend Server

## Run TensorFlow Serving
Start container and open the REST API port:
```
docker run -t --rm -p 8501:8501 \
    -v "$(pwd)/model:/models/model/1" \
    tensorflow/serving &
```