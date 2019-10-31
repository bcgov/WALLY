#!/bin/bash
WALLY_DATA_DIR=${WALLY_DATA_DIR-/wally_data}

ogr2ogr -f "PostgreSQL" PG:"host=$POSTGRES_SERVER port=5432 dbname=wally user=wally password=$POSTGRES_PASSWORD" "$WALLY_DATA_DIR/$1.geojson" -nln $1 -t_srs EPSG:4326 -append -progress -skipfailures --config OGR_TRUNCATE YES --config PG_USE_COPY YES
