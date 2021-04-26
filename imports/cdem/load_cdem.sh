#!/bin/bash
# USAGE: ./load_cdem.sh
# Loads CDEM raster data into the postgres db
#

set -euo pipefail
cd /dataload

pg_host="postgres://wally:$POSTGRES_PASSWORD@$POSTGRES_SERVER:5432/wally"

echo "(1/3) Setting up Minio host"
mc --config-dir=./.mc config host add minio http://${MINIO_HOST_URL} "$MINIO_ACCESS_KEY" "$MINIO_SECRET_KEY"

echo "(2/3) Copying CDEM raster data from Minio"
mc --config-dir=./.mc cp "minio/raster/BC_Area_CDEM.tif" "./"

echo "(3/3) Loading raster data into database $POSTGRES_SERVER"
raster2pgsql -s 4140 -t 100x100 -I -C -Y "./BC_Area_CDEM.tif" dem.cdem | psql "$pg_host"

echo "Finished."
