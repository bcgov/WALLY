#!/bin/bash
# USAGE: ./create_tileset.sh <mapbox source id>

set -e
# cd /dataload

mapbox_layer_id="$1"

declare -a layers=($(psql -X -A -t "postgres://wally:$POSTGRES_PASSWORD@$POSTGRES_SERVER:5432/wally" \
  --single-transaction \
  --field-separator=' ' \
  -c "SELECT ds.data_table_name
      FROM metadata.display_catalogue AS dc
      JOIN metadata.data_source AS ds ON dc.data_source_id = ds.data_source_id
      WHERE dc.mapbox_source_id='$1';"))

[ "${layers[@]}" = ""] && echo "no layers found for tileset $1. Check the mapbox_source_id value for metadata.display_catalogue" && exit 1

# build list of mbtiles to join
# layer_files=()
# for l in "${layers[@]}"; do layer_files+=("$l.mbtiles"); done

echo "Setting up Minio host"
mc --config-dir=./.mc config host add minio http://localhost:9000 "$MINIO_ACCESS_KEY" "$MINIO_SECRET_KEY"

for layer in "${layers[@]}"
do
  :
  echo "Downloading $layer"
  mc --config-dir=./.mc cp "minio/mbtiles/$layer.mbtiles" "./"
done

tile-join -o "$mapbox_layer_id.mbtiles" ./*.mbtiles

echo "Copying mbtileset to Minio storage..."
mc --config-dir=./.mc cp "./$mapbox_layer_id.mbtiles" "minio/tilestaging/$mapbox_layer_id.mbtiles"

echo "Uploading $mapbox_layer_id.mbtiles to Mapbox using $mapbox_layer_id"
mapbox --access-token "$MAPBOX_UPLOAD_TOKEN" upload "$mapbox_layer_id" "$mapbox_layer_id.mbtiles"

echo "Finished."
