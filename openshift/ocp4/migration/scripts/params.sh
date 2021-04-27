
#!/bin/bash

# ---------------------------------------------------------------------------------
# Set variables and get authentication
# ---------------------------------------------------------------------------------

# get params
ENVIRONMENT=${ENVIRONMENT:-$1}
# secret database-user
MATOMO_USER=${MATOMO_USER:-$2}
# secret database-password
MATOMO_PASSWORD=${MATOMO_PASSWORD:-$3}

# secret database-user
MATOMO_4_USER=${MATOMO_4_USER:-$4}
# secret database-password
MATOMO_4_PASSWORD=${MATOMO_4_PASSWORD:-$5}

# Ask what environment we're migrating
if [[ -z "$ENVIRONMENT" ]]; then
  read -r -p 'Namespace [test/prod]: ' ENVIRONMENT
fi

# Ask matomo db user
if [[ -z "$MATOMO_USER" ]]; then
  read -r -p 'pathfinder matomo db user: ' MATOMO_USER
fi
# Ask matomo db user password
if [[ -z "$MATOMO_PASSWORD" ]]; then
  read -r -p 'pathfinder matomo db password: ' MATOMO_PASSWORD
fi

# Ask matomo db user
if [[ -z "$MATOMO_4_USER" ]]; then
  read -r -p 'silver matomo db user: ' MATOMO_4_USER
fi
# Ask matomo db user password
if [[ -z "$MATOMO_4_PASSWORD" ]]; then
  read -r -p 'silver matomo db password: ' MATOMO_4_PASSWORD
fi

# Pathfinder namespace
NAMESPACE="bfpeyx-$ENVIRONMENT"

# Silver namespace
NAMESPACE4="d1b5d2-$ENVIRONMENT"

DB_DUMPFILE="/tmp/matomo-$ENVIRONMENT-mariadb-backup.sql"
