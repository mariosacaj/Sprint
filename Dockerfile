FROM python:3.7

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

RUN apt-get update --fix-missing && apt-get upgrade -y &&\
    apt-get install -y openjdk-11-jdk && \
    apt-get clean

