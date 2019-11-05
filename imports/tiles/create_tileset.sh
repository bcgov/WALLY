#!/bin/bash
# USAGE: ./create_tileset.sh <layer_name>
# use only the layer name. The layer name MUST be the layer name as spelled in the Wally database table.
# check the db table name or the __tablename__ of the SQLAlchemy model in the `wally/backend/app/layers` files.
# There should be an identically spelled <layer_name>.zip file available on the S3 storage configured below.
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

echo "Copying layer from Minio storage..."
./mc --config-dir=./.mc cp "minio/geojson/$1.zip" "./"

echo "Converting to mbtiles"

unzip -p "./$1.zip" | tippecanoe -zg --exclude-all -o ./$1.mbtiles --drop-densest-as-needed

echo "Copying $1.mbtiles to Minio storage..."
./mc --config-dir=./.mc cp "./$1.mbtiles" "minio/mbtiles"

echo "Finished."
