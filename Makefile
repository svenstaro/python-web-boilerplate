default: venv

venv:
	pyvenv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt -r dev-requirements.txt --upgrade

test: venv
	source ./dev_env.sh && venv/bin/pytest

docker_test:
	# Used to automatically run docker-compose to lint and test this
	# application inside a production-like environment.
	docker-compose pull
	docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit --force-recreate --remove-orphans
	docker-compose -f docker-compose.test.yml rm -f -v
	# docker-compose -f docker-compose.test.yml down --rmi local -v
	# in docker 1.13 use: docker system prune -a

_inside_docker_test_commands:
	# These commands are run inside of docker. They may or may not be safe to
	# run outside of the container context.
	flake8
	pytest

lint: venv
	source ./dev_env.sh && venv/bin/flake8

clean:
	rm -rf venv
