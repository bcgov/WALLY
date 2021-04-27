#!/bin/bash
# Usage: ./db_copy_and_restore.sh [test/prod]
# This script copies the dump from the matomo-migrator-cli volume to the db volume and restores the database using pg_restore

# Get variables from previous scripts or params
ENVIRONMENT=${ENVIRONMENT:-$1}
. ./params.sh "$ENVIRONMENT"
. ./require_silver_auth.sh

# Start copy to db pod and restore
MATOMO4_DB_POD=$(oc --kubeconfig="$KUBECONFIGSILVER" get pods -n "$NAMESPACE4" | grep "matomo-db" | grep Running | head -1 | awk '{print $1}')

echo "------------------------------------------------------------------------------"
echo "Found pod $MATOMO4_DB_POD on $NAMESPACE4"
echo "Starting copy to matomo-db pod..."
echo "------------------------------------------------------------------------------"

# Copy to db pod
SECONDS=0
oc --kubeconfig="$KUBECONFIGSILVER" -n "$NAMESPACE4" rsync /tmp/backup/ "$MATOMO4_DB_POD":/tmp/backup/
duration=$SECONDS
echo "------------------------------------------------------------------------------"
echo "Copy took $((duration / 60)) minutes and $((duration % 60)) seconds."
echo "Starting matomo mysql database insert..."
echo "------------------------------------------------------------------------------"

# Reload database
SECONDS=0
oc --kubeconfig="$KUBECONFIGSILVER" exec -n "$NAMESPACE4" "$MATOMO4_DB_POD" -c "mysql -u $MATOMO_4_USER -p$MATOMO_4_PASSWORD" -- bash -c "drop database matomo;" -c "create database matomo;" -c "matomo < $DB_DUMPFILE"

duration=$SECONDS
echo "------------------------------------------------------------------------------"
echo "Reload took $((duration / 60)) minutes and $((duration % 60)) seconds."
echo "Matomo database migration done. Please continue setting up matomo using the web GUI."
echo "------------------------------------------------------------------------------"