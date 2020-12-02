FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY requirements.txt /app/requirements.txt
COPY ./app /app

RUN pip install -r requirements.txt