#!/bin/bash
# Usage ./do_migration.sh 

# ---------------------------------------------------------------------------------
# Require all needed input/params for migration
# ---------------------------------------------------------------------------------
# running source on params.sh takes care of all needed parameters
# First thing it does is ask what environment we're doing the migration for
. ./params.sh

# Require login upfront
. ./require_pathfinder_auth.sh
. ./require_silver_auth.sh

# Dump and copy the matomo mysql database .sql file 
# from Pathfinder to the migrator pod
. ./matomo_db_dump_and_copy.sh

# Copy and restore the matomo mysql database .sql file 
# from the migrator pod to Silver matomo-db
. ./matomo_db_copy_and_restore.sh
