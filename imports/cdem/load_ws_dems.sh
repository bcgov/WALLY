#!/bin/bash
# USAGE: ./load_ws_dems.sh
# Loads pre-processed DEMs (CDEM/SRTM) for watershed delineation
# into the backend pod.

set -euo pipefail
mkdir -p /waterdata/rasters
cdem_file="Burned_CDEM_BC_Area_4326.tif"
srtm_file="Burned_SRTM_BC_48_51_3005.tif"

echo "(1/3) Setting up Minio host"
mc --config-dir=./.mc config host add minio "${MINIO_HOST_URL}" "$MINIO_ACCESS_KEY" "$MINIO_SECRET_KEY"

mc --config-dir=./.mc cp "minio/raster/$cdem_file" "/waterdata/rasters"
echo "Burned CDEM loaded to /waterdata/rasters/$cdem_file"

mc --config-dir=./.mc cp "minio/raster/$srtm_file" "/waterdata/rasters"
echo "Burned SRTM loaded to /waterdata/rasters/$srtm_file"
