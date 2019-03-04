default: init

init:
	poetry install

test: init
	poetry run pytest

lint: init
	poetry run flake8
