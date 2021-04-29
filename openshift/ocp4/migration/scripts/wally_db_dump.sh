#!/bin/bash
# Usage: ./wally_db_dump.sh [test/prod]

# This script dumps the old database and copies it to the migrator-cli's volume

# Get variables from previous scripts or params
ENVIRONMENT=${ENVIRONMENT:-$1}
. ./params.sh "$ENVIRONMENT"
. ./require_pathfinder_auth.sh


# Start dump and copy
WALLY_DB_POD=$(oc --kubeconfig="$KUBECONFIG" get pods -n "$NAMESPACE" | grep "wally-psql-$POD_SUFFIX" | head -1 | awk '{print $1}')

# Get leader or running pod
LEADER_OR_RUNNING=$(oc --kubeconfig="$KUBECONFIG" -n $NAMESPACE exec $WALLY_DB_POD -c postgresql -- patronictl list | awk '/Leader|running/{print $4}' | awk 'NR==1{print $1}')
echo "------------------------------------------------------------------------------"
echo "Found pod $LEADER_OR_RUNNING on $NAMESPACE"
echo "Starting database dump..."
echo "------------------------------------------------------------------------------"

# On Pathfinder - dump db
SECONDS=0
oc --kubeconfig="$KUBECONFIG" exec -n "$NAMESPACE" "$LEADER_OR_RUNNING" -- bash -c "pg_dump wally -a -t user -t user_map_layer -t project -t saved_analysis> $DB_DUMPFILE_WALLY"
duration=$SECONDS
echo "------------------------------------------------------------------------------"
echo "Dump took $((duration / 60)) minutes and $((duration % 60)) seconds."
echo "Starting to copy dumpfile from Pathfinder to this pod's volume..."
echo "------------------------------------------------------------------------------"

# In Migrator - copy file from Pathfinder
mkdir -p /tmp/backup
SECONDS=0
oc --kubeconfig="$KUBECONFIG" -n "$NAMESPACE" cp -c postgresql "$LEADER_OR_RUNNING":"$DB_DUMPFILE_WALLY" $DB_DUMPFILE_WALLY4
duration=$SECONDS
echo "------------------------------------------------------------------------------"
echo "Copy took $((duration / 60)) minutes and $((duration % 60)) seconds."
