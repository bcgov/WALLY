#!/bin/bash
# USAGE: ./load_hydrosheds
# Load Hydroshed polygons.
# Hydrosheds come in two datasets - "ar" (Arctic?) and "na" (North America?).
# This script loads them both and combines them into the existing table
# hydrosheds.hybas_lev12_v1c (defined and created by the WALLY backend database schema/migrations)
#
# https://www.hydrosheds.org/
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
./mc --config-dir=./.mc config host add minio "$MINIO_HOST_URL" "$MINIO_ACCESS_KEY" "$MINIO_SECRET_KEY"

echo "Copying layer from Minio storage..."
./mc --config-dir=./.mc cp "minio/other/hydrosheds.zip" "./"

echo "Loading data with ogr2ogr"

ogr2ogr \
  -f PostgreSQL \
  "PG:host=$POSTGRES_SERVER user=wally dbname=wally port=5432 password=$POSTGRES_PASSWORD" \
  -t_srs EPSG:3005 \
  -lco OVERWRITE=YES \
  -lco SCHEMA=hydrosheds \
  -lco GEOMETRY_NAME=geom \
  -nlt PROMOTE_TO_MULTI \
  -progress \
  "/vsizip/hydrosheds.zip/hybas_ar_lev12_v1c/hybas_ar_lev12_v1c.shp"

ogr2ogr \
  -f PostgreSQL \
  "PG:host=$POSTGRES_SERVER user=wally dbname=wally port=5432 password=$POSTGRES_PASSWORD" \
  -t_srs EPSG:3005 \
  -lco OVERWRITE=YES \
  -lco SCHEMA=hydrosheds \
  -lco GEOMETRY_NAME=geom \
  -nlt PROMOTE_TO_MULTI \
  -progress \
  "/vsizip/hydrosheds.zip/hybas_na_lev12_v1c/hybas_na_lev12_v1c.shp"

psql "postgres://wally:$POSTGRES_PASSWORD@$POSTGRES_SERVER:5432/wally" -c "ALTER TABLE hydrosheds.hybas_ar_lev12_v1c drop column ogc_fid"
psql "postgres://wally:$POSTGRES_PASSWORD@$POSTGRES_SERVER:5432/wally" -c "ALTER TABLE hydrosheds.hybas_na_lev12_v1c drop column ogc_fid"
psql "postgres://wally:$POSTGRES_PASSWORD@$POSTGRES_SERVER:5432/wally" -c "TRUNCATE hydrosheds.hybas_lev12_v1c"
psql "postgres://wally:$POSTGRES_PASSWORD@$POSTGRES_SERVER:5432/wally" -c "INSERT INTO hydrosheds.hybas_lev12_v1c SELECT * FROM hydrosheds.hybas_ar_lev12_v1c"
psql "postgres://wally:$POSTGRES_PASSWORD@$POSTGRES_SERVER:5432/wally" -c "INSERT INTO hydrosheds.hybas_lev12_v1c SELECT * FROM hydrosheds.hybas_na_lev12_v1c"
psql "postgres://wally:$POSTGRES_PASSWORD@$POSTGRES_SERVER:5432/wally" -c "DROP TABLE hydrosheds.hybas_na_lev12_v1c"
psql "postgres://wally:$POSTGRES_PASSWORD@$POSTGRES_SERVER:5432/wally" -c "DROP TABLE hydrosheds.hybas_ar_lev12_v1c"

echo "Done."
