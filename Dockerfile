FROM python:3.10.7-slim-buster

WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN apt-get update
RUN pip install -r requirements.txt
COPY . /app

EXPOSE 5000