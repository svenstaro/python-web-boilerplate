# Python Web Boilerplate

[![Build Status](https://travis-ci.org/svenstaro/python-web-boilerplate.svg?branch=master)](https://travis-ci.org/svenstaro/python-web-boilerplate)

## About
This is a boilerplate project made using best practices for getting started quickly
in a new project. I made this for myself but maybe it will help someone else. Pull
requests and discussions on best practices welcome!

## Development setup

Install all dependencies into a virtualenv which will be managed by `pipenv`.

    make

Set up your environment by sourcing copying `.env.example` to `.env`

    cp .env.example .env

For every new shell you need to source this file and you're good to go.

Make sure you have a working local postgres setup. Your current user should be
admin in your development postgres installation and it should use the "peer" or
"trust" auth methods (see `pg_hba.conf`). Given that, create a local
development database with some test data:

    flask initdb

Afterwards, type

    flask run

to run the development server.
