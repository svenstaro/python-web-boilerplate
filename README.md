# Python Web Boilerplate


## About
This is a boilerplate project made using best practices for getting started quickly.

Technologies used:
1. [FastAPI](https://fastapi.tiangolo.com/)
2. [ORM](https://github.com/encode/orm)
3. [Pytest](https://docs.pytest.org/en/stable/)
4. [Prometheus](https://prometheus.io/)

## Local execution with
1. if no env variables are provided, the script will spin up postgres docker container and app will connect to it: `make docker-run`
2. to provide different settings, set variables:
```
export <VARIABLE>=<YOUR_VALUE>

list of variables:
app_name
secret
hash_algo: check passlib algorithms list
db_host
db_port
db_user
db_password
db_database
```
and run: `make run-app`
Once the app is running

1. Swagger can be found on `localhost:5000/docs`
2. Prometheus metrics on `localhost:5000/metrics`

## Running the tests

run `make docker-test`
