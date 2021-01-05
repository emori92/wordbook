# Python
FROM python:3.7.9-buster

# version
LABEL imageversion=0.1

# working directory
WORKDIR /usr/src/app

# python encode
ENV PYTHONDONTWRITEBYTECODE 1 && \
    PYTHONUNBUFFERED 1

# copy file
COPY . /usr/src/app

# pip
RUN pip install -U pip && \
    pip install -r requirements.txt
