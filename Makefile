default: init

init:
	poetry install

test: init
	poetry run pytest

lint: init
	poetry run flake8

.PHONY: run-app
run-app:
	docker build -t boilerplate . && docker run -p 5000:5000 --env app_name --env secret --env hash_algo --env db_host --env db_port --env db_user --env db_password --env db_database


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


.PHONY: docker-test
docker-test:
	docker-compose down
	docker-compose up -d postgres
	sleep 3
	docker-compose up --build test
	docker-compose down
