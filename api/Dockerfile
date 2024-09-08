FROM python:3.11-rc-slim

RUN apt-get update -y && apt-get install -y build-essential python-dev libpq-dev
WORKDIR /api
COPY . /api
RUN pip3 install --upgrade pip -r requirements.txt
EXPOSE 5000