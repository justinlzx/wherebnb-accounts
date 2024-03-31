FROM python:3-slim

ARG PASSWORD="wherebnb"
ARG PUBLIC_IP_ADDRESS="34.173.224.187"
ARG DBNAME="accounts"
ARG PROJECT_ID="useful-memory-414316"
ARG INSTANCE_NAME="wherebnb-dev-db"

RUN apt-get update \
    && apt-get install -y libmariadb-dev-compat pkg-config build-essential \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./account.py .
EXPOSE 5000
CMD [ "python", "./account.py" ]
