default: init

init:
	pip install --upgrade pipenv
	pipenv install --dev

test: init
	pipenv run pytest

lint: init
	pipenv run flake8
