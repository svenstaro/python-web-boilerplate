default: init

init:
	poetry install

test: init
	poetry run pytest

lint: init
	poetry run flake8

.PHONY: docker-run
docker-run:
	docker build --no-cache -t python-boilerplate . && docker run --rm -it -p 5000:5000 --name python-boilerplate python-boilerplate
