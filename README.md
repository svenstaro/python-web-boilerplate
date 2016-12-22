# Python Web Template

## Development setup

Install all dependencies into a virtualenv which will be created at `venv/`:

  make

Set up your environment by sourcing `dev_env.sh`.

  source dev_env.sh

For every new shell you need to source this file and you're good to go.

Make sure you have a working local postgres setup. Your current user should be
admin in your development postgres installation and it should use the "peer" or
"trust" auth methods (see `pg_hba.conf`). Given that, create a local
development database with some test data:

  flask initdb

Afterwards, type

  flask run

to run the development server.
