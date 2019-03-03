help:
	less help-msg

dev: build-dev down-dev run-dev

web-dev: build-web-dev down-dev run-web-dev

prod: build-prod down-prod run-prod

html:
	python3 transform_md_to_html.py

# DEV

build-dev:
	docker-compose build

run-dev:
	docker-compose up

down-dev:
	docker-compose down -v

# PURE WEB DEV

build-web-dev:
	docker-compose build mongo mongo-express rabbit postgres web celery

run-web-dev:
	docker-compose up mongo mongo-express rabbit postgres web celery

# PROD

build-prod:
	docker-compose -f docker-compose.prod.yml build

run-prod:
	grep changeme .env && { echo "YOU NEED TO SET PROPER DB PASSWORDS"; exit 1 ;} || true
	docker-compose -f docker-compose.prod.yml up

down-prod:
	docker-compose -f docker-compose.prod.yml down -v

# UTILS

django-shell:
	docker-compose exec web python manage.py shell

bash:
	docker-compose exec web bash

test:
	echo "NO TESTS"

## static code analysis
static_test: test-static-db_maintainer test-static-web_api test-static_tests test-static-usage_examples	

test-static-db_maintainer:
	docker run -v $(shell pwd):/code -ti puchtaw/pylinter:latest database_maintainer/src

test-static-web_api:
	docker run -v $(shell pwd):/code -ti puchtaw/pylinter:latest web_api/src

test-static_tests:
	docker run -v $(shell pwd):/code -ti puchtaw/pylinter:latest tests || true  ## don`t fail for now - TO BE FIXED

test-static-usage_examples:
	docker run -v $(shell pwd):/code -ti puchtaw/pylinter:latest usage_examples || true  ## don`t fail for now - TO BE FIXED
