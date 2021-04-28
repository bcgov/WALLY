#!/bin/bash
# Usage: ./db_copy_and_restore.sh [test/prod]
# This script copies the dump from the migrator-cli volume to the db volume and restores the database using pg_restore

# Get variables from previous scripts or params
ENVIRONMENT=${ENVIRONMENT:-$1}
. ./params.sh "$ENVIRONMENT"
. ./require_silver_auth.sh

# Start copy to db pod and restore
WALLY4_DB_POD=$(oc --kubeconfig="$KUBECONFIGSILVER" get pods -n "$NAMESPACE4" | grep "wally-psql" | grep Running | head -1 | awk '{print $1}')

echo "------------------------------------------------------------------------------"
echo "Found pod $WALLY4_DB_POD on $NAMESPACE4"
echo "Starting copy to wally-psql pod..."
echo "------------------------------------------------------------------------------"

# Copy to db pod
SECONDS=0
oc --kubeconfig="$KUBECONFIGSILVER" -n "$NAMESPACE4" rsync /tmp/backup/ "$WALLY4_DB_POD":/tmp/backup/
duration=$SECONDS
echo "------------------------------------------------------------------------------"
echo "Copy took $((duration / 60)) minutes and $((duration % 60)) seconds."
echo "Starting wally database insert..."
echo "------------------------------------------------------------------------------"

# Reload database
SECONDS=0
oc --kubeconfig="$KUBECONFIGSILVER" exec -n "$NAMESPACE4" "$WALLY4_DB_POD" -c postgresql -- bash -c "psql wally -c \"DELETE FROM user\""
oc --kubeconfig="$KUBECONFIGSILVER" exec -n "$NAMESPACE4" "$WALLY4_DB_POD" -c postgresql -- bash -c "psql wally -c \"DELETE FROM user_map_layer\""
oc --kubeconfig="$KUBECONFIGSILVER" exec -n "$NAMESPACE4" "$WALLY4_DB_POD" -c postgresql -- bash -c "psql wally -c \"DELETE FROM project\""
oc --kubeconfig="$KUBECONFIGSILVER" exec -n "$NAMESPACE4" "$WALLY4_DB_POD" -c postgresql -- bash -c "psql wally -c \"DELETE FROM saved_analysis\""

oc --kubeconfig="$KUBECONFIGSILVER" exec -n "$NAMESPACE4" "$WALLY4_DB_POD" -c postgresql -- bash -c "psql wally < $DB_DUMPFILE_WALLY4"

duration=$SECONDS
echo "------------------------------------------------------------------------------"
echo "Reload took $((duration / 60)) minutes and $((duration % 60)) seconds."
echo "DB inserts done"
echo "------------------------------------------------------------------------------"