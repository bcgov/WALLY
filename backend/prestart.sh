#! /usr/bin/env bash

# Let the DB start
python /app/app/db/wait_for_db.py

# Run migrations
alembic -c alembic/alembic.ini upgrade head
