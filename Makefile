MANAGE=django-admin.py


test:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testtask.settings $(MANAGE) test apps.task
	flake8 --exclude '*migrations*' apps

run:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testtask.settings $(MANAGE) runserver

syncdb:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testtask.settings $(MANAGE) syncdb --noinput --no-initial-data
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testtask.settings $(MANAGE) migrate
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testtask.settings $(MANAGE) assets build
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testtask.settings $(MANAGE) collectstatic --noinput








