#!/bin/bash
poetry config virtualenvs.create false
poetry install --no-ansi

# if [ "$ENV" = "TEST" ]; then 
# 	poetry install --no-ansi  
# else
# 	poetry install --no-dev --no-ansi
# fi
