#!/bin/bash
# Usage: ./db_dump_and_copy.sh [test/prod]

# This script dumps the old matomo mysql database and copies it to the migrator-cli's volume

# Get variables from previous scripts or params
ENVIRONMENT=${ENVIRONMENT:-$1}
. ./params.sh "$ENVIRONMENT"
. ./require_pathfinder_auth.sh

# Start dump and copy
MATOMO_DB_POD=$(oc --kubeconfig="$KUBECONFIG" get pods -n "$NAMESPACE" | grep "matomo-db" | head -1 | awk '{print $1}')
echo "------------------------------------------------------------------------------"
echo "Found pod $MATOMO_DB_POD on $NAMESPACE"
echo "Starting database dump..."
echo "------------------------------------------------------------------------------"

# On Pathfinder - dump db
SECONDS=0
oc --kubeconfig="$KUBECONFIG" exec -n "$NAMESPACE" "$MATOMO_DB_POD" -- bash -c "mysqldump --no-autocommit --single-transaction matomo -h matomo-db -u $MATOMO_USER -p$MATOMO_PASSWORD > $DB_DUMPFILE"

duration=$SECONDS
echo "------------------------------------------------------------------------------"
echo "Dump took $((duration / 60)) minutes and $((duration % 60)) seconds."
echo "Starting to copy dumpfile from Pathfinder to this pod's volume..."
echo "------------------------------------------------------------------------------"

# In Migrator - copy file from Pathfinder
mkdir -p /tmp/backup
SECONDS=0
oc --kubeconfig="$KUBECONFIG" rsync -n "$NAMESPACE" "$MATOMO_DB_POD":"$DB_DUMPFILE_MATOMO" /tmp/backup/
duration=$SECONDS
echo "------------------------------------------------------------------------------"
echo "Rsync took $((duration / 60)) minutes and $((duration % 60)) seconds."

# delete dump from source
echo "Cleanup - deleting dump from Pathfinder"
echo "------------------------------------------------------------------------------"

oc --kubeconfig="$KUBECONFIG" exec -n "$NAMESPACE" "$MATOMO_DB_POD" -- rm -f "$DB_DUMPFILE_MATOMO"

# Scale down the pathfinder matomo database DC
#oc --kubeconfig="$KUBECONFIG" -n "$NAMESPACE" scale --replicas=0 "dc/matomo-db"