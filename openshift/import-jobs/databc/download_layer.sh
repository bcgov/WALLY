#!/bin/bash
# download_layer.sh
# Use for downloading GeoJSON layer data when a zipped direct download link is available. The zip file
# will be stored in the s3 storage (configured below - see Setting up Minio host) as <layer_table_name>.zip. 
#
# USAGE: ./download_layer.sh <layer_name> <url>
# use the layer name from the Wally DB table that the data should be loaded into. You can check the database
# or the SQLAlchemy model __tablename__ in `wally/backend/app/layers`.
#
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

echo "downloading $1 from $2"
curl -o "$1.zip" "$2"

echo "Copying zipped layer to Minio storage..."
./mc --config-dir=./.mc cp "./$1.zip" "minio/geojson"

echo "Finished."
