web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 2
worker: celery -A app.celery worker --loglevel=info
beat: celery -A app.celery beat --loglevel=info
release: flask db upgrade
