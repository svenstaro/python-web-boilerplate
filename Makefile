default: venv

venv:
	pyvenv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt -r dev-requirements.txt --upgrade

test: venv
	source ./dev_env.sh && venv/bin/pytest

lint: venv
	source ./dev_env.sh && venv/bin/flake8

clean:
	rm -rf venv
