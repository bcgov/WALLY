#! /usr/bin/env bash

# Let the DB start
python /app/app/db/wait_for_db.py

# Uncomment this line and start the docker-compose stack to create a merge revision.
# alembic -c alembic/alembic.ini merge heads -m 'merge migrations'

# Run migrations
alembic -c alembic/alembic.ini upgrade head
