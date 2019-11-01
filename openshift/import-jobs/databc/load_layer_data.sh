#!/bin/bash
# USAGE: ./load_layer_data.sh <layer_name>
# use only the layer name. There should be a <layer_name>.zip file available on the S3 storage configured below.
# The environment must have the following env variables:
# MINIO_ACCESS_KEY
# MINIO_SECRET_KEY
# POSTGRES_SERVER
# POSTGRES_PASSWORD
# The database name is assumed to be "wally".

set -e
cd /dataload
echo "Setting up Minio host"
mc config host add minio http://minio:9000 "$MINIO_ACCESS_KEY" "$MINIO_SECRET_KEY"

echo "Copying layer from Minio storage..."
mc cp "minio/geojson/$1.zip" "./"

echo "Loading data with ogr2ogr"
ogr2ogr -f "PostgreSQL" PG:"host=$POSTGRES_SERVER port=5432 dbname=wally user=wally password=$POSTGRES_PASSWORD" "./$1.zip/$1.geojson" -nln $1 -t_srs EPSG:4326 -append -progress -skipfailures --config OGR_TRUNCATE YES --config PG_USE_COPY YES

echo "Finished."