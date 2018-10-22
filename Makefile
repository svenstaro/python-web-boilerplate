default: init

init:
	pip install pipenv
	pipenv install --dev

test: init
	pipenv run pytest

lint: init
	pipenv run flake8
