FROM python:3.6-slim

RUN apt-get update && apt-get install -qq -y \
  build-essential libpq-dev --no-install-recommends

RUN mkdir -p /app
WORKDIR /app
COPY src/ /app/

# ENV DJANGO_SETTINGS_MODULE=jobsite.settings
COPY src/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src/ .
