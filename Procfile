web: gunicorn spaceport:app
web: flower --port=$PORT --broker=$BROKER_URL --db=$DATABASE_URL --persistent=true --basic_auth=$FLOWER_AUTH
worker: celery worker -A job.app -l INFO --concurrency=1