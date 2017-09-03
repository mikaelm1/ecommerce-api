#!/bin/sh

# wait for Reddis server to start
sleep 1
# echo "INSIDE RUN CELERY SCRIPT========================================"
# ls
cd src
# echo "CHANGED DIRS"
# ls core/
pwd  
# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
# celery worker -A ecommerce.celery -l info