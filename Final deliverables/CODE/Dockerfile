FROM python:3.8.8

WORKDIR /app

ADD . /first_flask_project

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /app
