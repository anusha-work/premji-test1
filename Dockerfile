FROM python:3.11-alpine

RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN apk update \
  && apk add \
    build-base \
    postgresql \
    postgresql-dev \
    libpq



ENV PYTHONUNBUFFERED 1

COPY . .