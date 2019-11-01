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
./mc --config-dir=./.mc config host add minio http://minio:9000 "$MINIO_ACCESS_KEY" "$MINIO_SECRET_KEY"

echo "renaming layer to $1"
curl -o "$1.zip" "$2"

echo "Copying zipped layer to Minio storage..."
./mc --config-dir=./.mc cp "./$1.zip" "minio/geojson"

echo "Finished."
