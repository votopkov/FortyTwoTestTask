MANAGE=django-admin.py


test:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testtask.settings $(MANAGE) test apps.task

run:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testtask.settings $(MANAGE) runserver

syncdb:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testtask.settings $(MANAGE) syncdb --noinput --no-initial-data
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testtask.settings $(MANAGE) migrate
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testtask.settings $(MANAGE) collectstatic --noinput

flake8:
	flake8 --exclude '*migrations*' apps

functional_admin_test:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testtask.settings $(MANAGE) test apps.task.tests.selenium_admin_test

functional_test:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testtask.settings $(MANAGE) test apps.task.tests.selenium_test

dumpdata:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testtask.settings $(MANAGE) dumpdata -e admin -e contenttypes > apps/task/fixtures/initial_data.json





