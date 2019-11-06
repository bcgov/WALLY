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
# MAPBOX_ACCESS_TOKEN
# The database name is assumed to be "wally".

set -e
cd /dataload

# get metadata about this data source from Wally table metadata.data_source
declare -a row=($(psql -X -A -t "postgres://wally:$POSTGRES_PASSWORD@$POSTGRES_SERVER:5432/wally" \
  --single-transaction \
  --field-separator=' ' \
  -c "SELECT dc.mapbox_layer_id FROM metadata.display_catalogue AS dc JOIN metadata.data_source as ds on dc.data_source_id = ds.data_source_id WHERE ds.data_table_name='$1';"))

mapbox_layer_id="${row[0]}"

echo "Setting up Minio host"
./mc --config-dir=./.mc config host add minio http://minio:9000 "$MINIO_ACCESS_KEY" "$MINIO_SECRET_KEY"

echo "Copying mbtileset from Minio storage..."
./mc --config-dir=./.mc cp "minio/mbtiles/$1.mbtiles" "./"

echo "Uploading $1.mbtiles to Mapbox using $mapbox_layer_id"
mapbox upload "$mapbox_layer_id" "$1.mbtiles"

echo "Finished."
