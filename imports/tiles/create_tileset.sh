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
# cd /dataload

# get metadata about this data source from Wally table metadata.data_source
declare -a row=($(psql -X -A -t "postgres://wally:$POSTGRES_PASSWORD@$POSTGRES_SERVER:5432/wally" \
  --single-transaction \
  --field-separator=' ' \
  -c "SELECT dc.display_data_name, dc.required_map_properties
      FROM metadata.display_catalogue AS dc
      JOIN metadata.data_source as ds on dc.data_source_id = ds.data_source_id
      WHERE ds.data_table_name='$1';"))

mapbox_layer_name="${row[0]}"

echo "using layer name: $mapbox_layer_name"
map_properties=$(echo "${row[1]}" | tr -d '{' | tr -d '}')


# determine zoom level
# if we are going to combine these tiles, they need to use the same zoom level.
# use the zoom level listed for the mapbox source ID.
declare -a zoom=($(psql -X -A -t "postgres://wally:$POSTGRES_PASSWORD@$POSTGRES_SERVER:5432/wally" \
  --single-transaction \
  --field-separator=' ' \
  -c "SELECT ms.max_zoom
      FROM metadata.display_catalogue AS dc
      JOIN metadata.data_source as ds on dc.data_source_id = ds.data_source_id
      JOIN metadata.mapbox_source AS ms ON ms.mapbox_source_id = dc.mapbox_source_id
      WHERE ds.data_table_name='$1';"))

# default to automatically choose zoom level. will result in different max zoom levels if different
# layers automatically choose their own zoom level, so this is only a good default if we don't plan
# to combine this layer with others (joined layers need to have the same zoom level).
tippecanoe_zoom_level="-zg"

# if a zoom level was found, it will be in zoom[0]. Check if exists and then set the -z arg accordingly.
[ "${zoom[0]}" != "" ] && tippecanoe_zoom_level="-z${zoom[0]}"

# extra arguments - for excluding all properties (default) or
# adding in properties one by one (if present in $map_properties)
extra_args="-X"

if [[ $map_properties != "" ]]
then
  # construct extra args in the form of "-y POD_SUBTYPE -y LICENCE_NUMBER" etc
  echo "$map_properties"
  extra_args=$(echo "$map_properties" | sed "s/,/ -y /g" | sed "s/^/-y /")
fi

echo "using zoom level for $mapbox_layer_name: $tippecanoe_zoom_level"
echo "using extra arguments for $mapbox_layer_name: $extra_args"

echo "Setting up Minio host"
mc --config-dir=./.mc config host add minio http://localhost:9000 "$MINIO_ACCESS_KEY" "$MINIO_SECRET_KEY"

echo "Copying layer from Minio storage..."
mc --config-dir=./.mc cp "minio/geojson/$1.zip" "./"

echo "Converting to mbtiles using layer name $mapbox_layer_name"

# https://github.com/mapbox/tippecanoe
# -zg : automatically choose the zoom levels points are visible at
# --force: overwrite existing mbtiles file
# -X: exclude all properties
# -y: include specific property
# -r1: prevent auto-grouping points 
unzip -p "./$1.zip" | tippecanoe "$tippecanoe_zoom_level" --force --layer="$mapbox_layer_name" -o "./$1.mbtiles" -r1 "$extra_args"

echo "Copying $1.mbtiles to Minio storage..."
mc --config-dir=./.mc cp "./$1.mbtilessdf" "minio/mbtilesdfgdfg"

echo "Finished."
