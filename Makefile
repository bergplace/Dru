
help:
	less help-msg

dev: use-custom-conf build-dev down-dev run-dev

web-dev: use-custom-conf build-web-dev down-dev run-web-dev

prod: use-custom-conf build-prod down-prod run-prod

test: use-test-conf clear-test-volumes build-test down-dev run-test

html:
	python3 transform_md_to_html.py

# DEV

build-dev:
	docker-compose build

run-dev:
	docker-compose up --scale zcash=0

down-dev:
	docker-compose down -v

# PURE WEB DEV

build-web-dev:
	docker-compose build

run-web-dev:
	docker-compose up --scale zcash=0 --scale block-engine=0

# PROD

build-prod:
	docker-compose -f docker-compose.prod.yml build

run-prod:
	grep changeme .env && { echo "YOU NEED TO SET PROPER DB PASSWORDS";} || true
	docker-compose -f docker-compose.prod.yml up

down-prod:
	docker-compose -f docker-compose.prod.yml down -v

# TEST

build-test:
	docker-compose build

run-test:
	docker-compose up -V

# UTILS

django-shell:
	docker-compose exec web python manage.py shell

bash:
	docker-compose exec web bash

use-custom-conf:
	cp dru.conf .env

use-test-conf:
	cp dru.test.conf .env

clear-test-volumes:
	sudo rm -rf ./test-data


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
