#!/bin/bash
poetry config virtualenvs.create false
poetry install --no-ansi


# TODO: it would make sense to build dev dependecies in test execution only
# if [ "$ENV" = "TEST" ]; then 
# 	poetry install --no-ansi  
# else
# 	poetry install --no-dev --no-ansi
# fi
