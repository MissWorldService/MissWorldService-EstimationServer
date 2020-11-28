# MissWorldService-EstimationServer
Python Backend Server

## How to run
Start TensorFlow Serving container and open the REST API port
```
docker run -t --rm -p 8501:8501 \
    -v "$(pwd)/models:/models" \
    -e MODEL_NAME=half_plus_two \
    tensorflow/serving &
```