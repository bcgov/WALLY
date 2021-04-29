#!/bin/bash
# USAGE: ./load_ws_dems.sh
# Loads pre-processed DEMs (CDEM/SRTM) for watershed delineation
# into the backend pod.

set -euo pipefail
mkdir -p /waterdata/rasters

echo "(1/3) Setting up Minio host"
mc --config-dir=./.mc config host add minio ${MINIO_HOST_URL} "$MINIO_ACCESS_KEY" "$MINIO_SECRET_KEY"

if [ ! -f "/waterdata/rasters/Burned_CDEM_BC_Area_4326.tif" ]; then
    echo "Burned CDEM file not found!"
    mc --config-dir=./.mc cp "minio/raster/Burned_CDEM_BC_Area_4326.tif" "/waterdata/rasters"
    echo "Burned CDEM loaded to /waterdata/rasters/Burned_CDEM_BC_Area_4326.tif"
fi

if [ ! -f "/waterdata/rasters/Burned_SRTM_BC_48_51_3005.tif" ]; then
    echo "Burned SRTM file not found!"
    mc --config-dir=./.mc cp "minio/raster/Burned_SRTM_BC_48_51_3005.tif" "/waterdata/rasters"
    echo "Burned SRTM loaded to /waterdata/rasters/Burned_SRTM_BC_48_51_3005.tif"
fi
