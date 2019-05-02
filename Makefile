
help:
	less help-msg

start: manage-conf build down run

start-detached: manage-conf build down run-detached

test: manage-test-conf build down run-detached sleep run-test

html:
	python3 transform_md_to_html.py

# START

manage-conf:
	./build-tools/cp_conf_if_not_exists.sh
	cp dru.conf .env
	python3 build-tools/manage-env.py

build:
	docker-compose build

down:
	docker-compose down -v

run:
	./build-tools/docker-compose-up.sh

run-detached:
	./build-tools/docker-compose-up.sh -d

# TEST

run-detached:
	docker-compose up -d

sleep:
	sleep 30

manage-test-conf:
	cp dru.test.conf .env
	python3 build-tools/manage-env.py


run-test:
	python3 -m unittest discover test

# UTILS

django-shell:
	docker-compose exec web python3 manage.py shell

bash:
	docker-compose exec web bash

# STATIC CODE ANALYSIS

static_test: test-static-db_maintainer test-static-web_api test-static_tests test-static-usage_examples	

test-static-db_maintainer:
	docker run -v $(shell pwd):/code -ti puchtaw/pylinter:latest database_maintainer/src

test-static-web_api:
	docker run -v $(shell pwd):/code -ti puchtaw/pylinter:latest web_api/src

test-static_tests:
	docker run -v $(shell pwd):/code -ti puchtaw/pylinter:latest tests || true  ## don`t fail for now - TO BE FIXED

test-static-usage_examples:
	docker run -v $(shell pwd):/code -ti puchtaw/pylinter:latest usage_examples || true  ## don`t fail for now - TO BE FIXED
