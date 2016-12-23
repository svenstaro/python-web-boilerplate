default: venv

venv:
	pyvenv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt --upgrade

test: install
	venv/bin/pytest

lint:
	venv/bin/flake8

clean:
	rm -rf venv
