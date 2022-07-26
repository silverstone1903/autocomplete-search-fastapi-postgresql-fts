FROM python:3.7-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./app ./app
COPY ./data ./data
COPY ./templates ./templates
COPY ./tests ./tests
RUN pip install -r app/requirements.txt  --no-cache-dir


