#!/bin/bash
# USAGE: ./load_layer_data.sh <layer_name>
# use only the layer name. The layer name MUST be the layer name as spelled in the Wally database table.
# check the db table name or the __tablename__ of the SQLAlchemy model in the `wally/backend/api/layers` files.
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

echo "Loading data with ogr2ogr"
unzip -p "./$1.zip" | ogr2ogr -f "PostgreSQL" PG:"host=$POSTGRES_SERVER port=5432 dbname=wally user=wally password=$POSTGRES_PASSWORD" /vsistdin/ -nln $1 -t_srs EPSG:4326 -append -progress -skipfailures --config OGR_TRUNCATE YES --config PG_USE_COPY YES

echo "Finished loading data. Updating Wally metadata table".

# get the date this data was last updated.  IMPORTANT: this is inferred by the Last Modified date on the source data from S3 storage.
# NOT the time when the data was loaded into the database.  This is to help prevent the date updated column being set to "now()" if
# the data being used is somehow out of date.
last_updated=$(./mc --config-dir=./.mc ls "minio/geojson/$1.zip" --json | jq .lastModified)

psql "postgres://wally:$POSTGRES_PASSWORD@$POSTGRES_SERVER:5432/wally" -c "UPDATE metadata.data_source SET last_updated_data = '$last_updated' WHERE data_table_name = '$1';"

echo "Finished."
