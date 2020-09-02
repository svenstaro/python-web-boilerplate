default: init

init:
	poetry install

test: init
	poetry run pytest

lint: init
	poetry run flake8

.PHONY: docker-run
docker-run:
	docker-compose down
	docker-compose up -d postgres
	sleep 3
	docker-compose up --build app

.PHONY: partial-restart
partial-restart:
	docker-compose stop app
	docker-compose up --build app
	# docker build --no-cache -t python-boilerplate . && docker run --rm -it -p 5000:5000 --name python-boilerplate --env db_host=postgres python-boilerplate
