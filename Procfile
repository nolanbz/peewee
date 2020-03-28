web: gunicorn app:job
worker: celery worker -A job.app -l INFO --concurrency=1