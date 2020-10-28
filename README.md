# Python Web Boilerplate


## About
This is a boilerplate project made using best practices for getting started quickly.

Technologies used:
1. [FastAPI](https://fastapi.tiangolo.com/)
2. [ORM](https://github.com/encode/orm)
3. [Pytest](https://docs.pytest.org/en/stable/)
4. [Prometheus](https://prometheus.io/)
5. [Passlib](https://passlib.readthedocs.io/en/stable/)

## Requirements
1. Docker
2. Postgres (optional)


## Local execution with
This application requires a postgres running somewhere. 
1. To start the application with a local postgres run `make run-app`
2. To start both app and postgres in containers run `make docker-run`

Once the app is running

1. Swagger can be found on `localhost:5000/docs`
2. Prometheus metrics on `localhost:5000/metrics`

Default settings:
1. passlib hash algo: argon2 

## Setup
Application will be searching for a configuration file `.env.<ENV>`

Example of a configuration file is provided under `.env.local`

Following configuration variables are expected:
```
app_name - name of the application to stat
hash_algo - passlib algorithms
db_host - postgres host, like postgres or localhost
db_port - 5432 most of the time for postgres
db_user - service user allowed to acces and write to postgres instance
db_password - password to access postgres instance
db_database - specific database to connect to and work with tables
```
and run: `make run-app`

## Running tests

run `make docker-test`
