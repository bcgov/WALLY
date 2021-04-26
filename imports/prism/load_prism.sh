#!/bin/bash
# USAGE: ./load_prism.sh <dataset code>
# valid dataset codes:
# pr - precipitation
#
# more datasets (tasmin and tasmax for daily min temp near surface and daily max temp near surface)
# can be supported by adding raster files to Minio using the following format:
# raster/prism_<dataset>.asc; raster/prism_<dataset>.prj
# e.g.:
# raster/prism_tasmin.asc raster/prism_tasmin.prj

set -euo pipefail
cd /dataload

dataset="$1"

pg_host="postgres://wally:$POSTGRES_PASSWORD@$POSTGRES_SERVER:5432/wally"

echo "(1/3) Setting up Minio host"
mc --config-dir=./.mc config host add minio http://${MINIO_HOST_URL}:9000 "$MINIO_ACCESS_KEY" "$MINIO_SECRET_KEY"

echo "(2/3) Copying PRISM raster data from Minio"
mc --config-dir=./.mc cp "minio/raster/prism_$dataset.asc" "./"
mc --config-dir=./.mc cp "minio/raster/prism_$dataset.prj" "./"

echo "(3/3) Loading raster data into database $POSTGRES_SERVER"
raster2pgsql -s 4326 -t 100x100 -I -C -Y "./prism_$dataset.asc" prism.prism | psql "$pg_host"

echo "Finished."
