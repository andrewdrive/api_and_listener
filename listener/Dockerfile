FROM python:3.8.10
ENV PYTHONUNBUFFERED=1
RUN apt-get update
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install --upgrade pip
RUN pip install kafka-python requests