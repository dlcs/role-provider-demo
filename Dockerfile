FROM python:3.10-slim-buster

RUN apt-get update -y && apt-get install -y build-essential

LABEL maintainer="Donald Gray <donald.gray@digirati.com>"
LABEL org.opencontainers.image.source=https://github.com/dlcs/role-provider-demo
LABEL org.opencontainers.image.description="Demonstrator app for DLCS role provider"

ENV PYTHONUNBUFFERED 1

WORKDIR /opt/app
COPY requirements.txt requirements.txt
COPY docker-requirements.txt docker-requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r docker-requirements.txt

COPY . .

CMD [ "uwsgi", "--plugins", "http,python3", \
               "--http", "0.0.0.0:80", \
               "--protocol", "uwsgi", \
               "--enable-threads", \
               "--master", \
               "--http-timeout", "600", \
               "--module", "main:app" ]
