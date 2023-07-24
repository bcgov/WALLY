
#!/bin/bash
# Usage: ./wally_migrate_user_data.sh

# Run the db migration scripts for user map layers

. ./wally_db_dump.sh
ls -alh /tmp/backup

echo "------------------------------------------------------------------------------"
echo "Copy from Pathfinder successful. Copying to the db pod and restoring the database..."
echo "------------------------------------------------------------------------------"

. ./wally_db_insert.sh