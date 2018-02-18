#!/bin/sh

# wait for Reddis server to start
sleep 1
cd src
# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
celery worker -A ecommerce.celery -l info