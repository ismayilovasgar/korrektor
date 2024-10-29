 
# #!/bin/bash

# # Django serverini işə salır
# echo "Django serveri işə salınır..."
# python manage.py runserver &

# # Celery workerini işə salır
# echo "Celery worker işə salınır..."
# celery -A core worker --loglevel=info &

# # Celery beat'i işə salır
# echo "Celery beat işə salınır..."
# celery -A core beat --loglevel=info &

# wait
