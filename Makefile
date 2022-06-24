run:
    python3 manage.py runserver

migrate:
    python3 manage.py makemigrations
    python3 manage.py migrate
runcelery:
	celery -A config worker -l info
