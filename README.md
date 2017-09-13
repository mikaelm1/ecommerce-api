# Overview

An open source Django backend API for ecommerce apps.

## Getting Started

1. [Install Docker](https://docs.docker.com/engine/installation/)
2. Clone the repo: `git clone https://github.com/mikaelm1/ecommerce-api.git`
3. Rename `src/ecommerce/settings/dev.py.example` to `src/ecommerce/settings/dev.py` and replace the `xxx` values with your proper values.
4. Renamce `.env.example` to `.env` and replace the `xxx` values with those from settings.
5. Run: `chmod +x run.sh` to make a helper script executable.
6. Run `./run.sh d` to start up the development environment.

## API Documentation

You can view all the routes available in the app by visiting: `localhost:8080`.

API documentation is built using DRF's [built-in documentation tool](http://www.django-rest-framework.org/topics/documenting-your-api/).

## Authentication

Authentication is done using [JWT](https://github.com/GetBlimp/django-rest-framework-jwt).

All auth protected routes must have the following in the header:
```
Authorization: JWT the_token_here
```

## Running Tests
To run all the tests in the project: `./run.sh t`

## Running in Production
The production environment uses gunicorn as the web server and nginx as a reverse proxy. 
1. Rename `docker-compose.prod.yml.example` to `docker-compose.prod.yml`
2. Run: `./run.sh p`