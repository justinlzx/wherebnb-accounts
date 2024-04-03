FROM python:3-slim

ARG PASSWORD
ARG PUBLIC_IP_ADDRESS
ARG DBNAME
ARG PROJECT_ID
ARG INSTANCE_NAME

RUN apt-get update \
    && apt-get install -y libmariadb-dev-compat pkg-config build-essential \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./account.py .
EXPOSE 5000
CMD [ "python", "./account.py" ]
