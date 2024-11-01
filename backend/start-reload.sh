#! /usr/bin/env sh
set -e

export APP_MODULE=${APP_MODULE:-"main:wally_api"}

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
LOG_LEVEL=${LOG_LEVEL:-info}

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
    python /app/api/initial_data.py
fi

# Start Uvicorn with live reload
exec uvicorn --reload --host $HOST --port $PORT --log-level $LOG_LEVEL "$APP_MODULE"
