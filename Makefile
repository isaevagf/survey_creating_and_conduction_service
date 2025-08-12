.PHONY: runserver migrate makemigrations shell clean

runserver:
	python manage.py runserver

migrate:
	python manage.py makemigrations surveys_creating
	python manage.py makemigrations surveys_conducting
	python manage.py makemigrations authorization
	python manage.py migrate

initdb:
	python manage.py loaddata initial_data/data

#dumpdata:
#	python -Xutf8 manage.py dumpdata --output initial_data/data.json