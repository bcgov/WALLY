#!/bin/bash
# download_and_zip_layer.sh
# Use for downloading GeoJSON layer data and then zipping contents when link is available. The zip file
# will be stored in the s3 storage (configured below - see Setting up Minio host) as <layer_table_name>.zip. 
#
# USAGE: ./download_and_zip_layer.sh <layer_name> <url>
# use the layer name from the Wally DB table that the data should be loaded into. You can check the database
# or the SQLAlchemy model __tablename__ in `wally/backend/api/layers`.
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
curl -Lo "$1.geojson" "$2"

echo "Zipping file $1.geojson"
zip "./out/$1.zip" "./out/$1.geojson"

echo "Copying zipped layer to Minio storage..."
./mc --config-dir=./.mc cp "./$1.zip" "minio/geojson"

echo "Finished."
