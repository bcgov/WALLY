#! /usr/bin/env sh
set -e

export APP_MODULE=${APP_MODULE:-"main:app"}

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
LOG_LEVEL=${LOG_LEVEL:-info}

export BACKEND_CORS_ORIGINS="http://localhost:8080, https://localhost, https://localhost:4200, https://localhost:3000, https://localhost:8080, http://dev.wally.pathfinder.gov.bc.ca, https://wally-staging.pathfinder.gov.bc.ca, https://wally.pathfinder.gov.bc.ca"
export MAPBOX_ACCESS_TOKEN=pk.eyJ1IjoiaWl0LXdhdGVyIiwiYSI6ImNrMHBrZzczZjBlZ2UzZG54NTZldTRtdmUifQ.70prUCk1zBMUFnqfDSywYg
export MAPBOX_STYLE=mapbox://styles/iit-water/ck22hx0391ch31dk9amwwr67x
export POSTGRES_SERVER=localhost:5432
export POSTGRES_USER=wally
export POSTGRES_PASSWORD=test_pw
export POSTGRES_DB=wally
# PROJECT_NAME=Wally
# API_SERVICE=backend:8000
# WALLY_ENV=DEV

# If there's a prestart.sh script in the /app directory, run it before starting
PRE_START_PATH=/app/prestart.sh
echo "Checking for script in $PRE_START_PATH"
if [ -f $PRE_START_PATH ] ; then
    echo "Running script $PRE_START_PATH"
    . "$PRE_START_PATH"
else 
    echo "There is no script $PRE_START_PATH"
fi

# Load fixture data for dev environments
if [ "$WALLY_ENV" = "DEV" ]; then
    python /app/app/initial_data.py
fi

source venv/bin/activate

# Merge Display Templates with existing templates
# python /app/app/merge_display_templates.py

# Start Uvicorn with live reload
exec uvicorn --reload --host $HOST --port $PORT --log-level $LOG_LEVEL "$APP_MODULE"
