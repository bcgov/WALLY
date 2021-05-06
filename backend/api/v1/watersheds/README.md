# Watersheds

Delineation of watersheds, summaries of watershed statistics, and aggregation of data pertaining to watersheds happens here.

## Spatial rasters


WALLY uses a number of spatial raster files containing data to help delineate watersheds as well as extract information like
aspect and solar exposure. These files are converted to Cloud Optimized GeoTIFFs (COG) and stored in Minio. Using GDAL's COG
support, we can store large GeoTIFFs that cover the full province, and WALLY can request parts of the file by bounding box
coordinates.

### 12 arcsecond CDEM

The 12 arcsecond CDEM is used for simple statistics like average elevation and slope.

* Download the file from https://ftp.maps.canada.ca/pub/nrcan_rncan/elevation/cdem_mnec/archive/ (cdem_12s.tif)
* Clip to an area around BC: 
```sh
gdalwarp -of "GTiff" -te -142 48 -112 62 ./cdem_12sec.tif ./BC_Area_CDEM.tif
```
* Store on Minio in the `raster` bucket.
* Use the import job `cdem.job.yaml` to import it to staging/production. See [the OCP4 migration README](../../../../openshift/ocp4/README.md) for detailed instructions.
* For local dev, a migration loads a Whistler area version. If you need to update it, look in the migrations.

### Preprocessed DEM with burned streams

Delineating watersheds requires a Digital Elevation Model (DEM) pre-processed to burn streams.  For watersheds in Canada, the CDEM 3 second DEM is used.
We also use the SRTM DEM along the border with Washington, Idaho and Montana.

#### CDEM
Download the 3 second DEM from https://ftp.maps.canada.ca/pub/nrcan_rncan/elevation/cdem_mnec/archive/

Download the Freshwater Atlas Stream Networks:
```sh
wget -r ftp://ftp.gdbc.gov.bc.ca/sections/outgoing/bmgs/FWA_Public/FWA_STREAM_NETWORKS_SP.gdb/
```

Clip DEM to BC:
```sh
gdalwarp t_srs EPSG:4326 -of "GTiff" -te -142 48 -112 62 ./cdem_3sec.tif ./BC_Area_CDEM_3sec_4326.tif
```

Convert FWA Streams to a shapefile:
```sh
ogr2ogr -f "ESRI Shapefile" -t_srs EPSG:4326 -select LINEAR_FEATURE_ID streams_4326.shp FWA_STREAM_NETWORKS_SP.gdb
```

Use WhiteboxTools to burn streams:
```sh
whitebox_tools -r=FillBurn -v --wd="./" --dem=BC_Area_CDEM_3sec_4326.tif --streams=streams_4326.shp -o=01_burned.tif
```

Convert to a COG:
```sh
gdal_translate "01_burned.tif" "Burned_CDEM_4326.tif" \
     -co TILED=YES -co BLOCKXSIZE=512 -co BLOCKYSIZE=512 \
     -co COMPRESS=LZW -co PREDICTOR=2 \
     -co COPY_SRC_OVERVIEWS=YES -co BIGTIFF=YES
```

Upload the resulting `Burned_CDEM_4326.tif` to Minio. This file is required by `backend/api/v1/watersheds/delineate_watersheds.py`.
Don't forget to [clip a copy to Whistler area](../../../fixtures/extents/README.md) and store it in `backend/fixtures/raster`.

#### SRTM

SRTM tiles are available from EarthExplorer.
You will need the BC streams file from above and the Washington streams file from https://geo.wa.gov/datasets/71fa52e7d6224fde8b09facb12b30f04_24.

We use 3005 for SRTM DEM's, but we may want to refactor to 4326 in the future.

After downloading tiles for the desired area, merge the HGT format tiles together.
```sh
gdalwarp -t_srs EPSG:3005 -r cubic -of "GTiff" *.hgt ../merged/srtm.tif
```


Create extents for the resulting raster in qGIS (Vector > Research > Extract extent) and store as clipsrc.shp.

Clip vector by extents:
```sh
# create overlays in projections matching BC and WA streams respectively (I happened to have BC Streams in 4326 and WA Streams in 3857)
ogr2ogr -s_srs "EPSG:3005" -t_srs "EPSG:4326" -f "ESRI Shapefile"  clipsrc_4326.shp clipsrc.shp
ogr2ogr -s_srs "EPSG:3005" -t_srs "EPSG:3857" -f "ESRI Shapefile"  clipsrc_3857.shp clipsrc.shp
ogr2ogr -f "ESRI Shapefile" -clipsrc clipsrc_4326.shp bc_streams_clipped.shp ../../streams/streams.shp 
ogr2ogr -f "ESRI Shapefile" -clipsrc clipsrc_3857.shp wa_streams_clipped.shp ../../WA_Streams/WA_Hydrography_-_NHD_Flowline-shp/WA_Hydrography_-_NHD_Flowline.shp
```

...and merge the streams together. You may need to install pygdal with `pip install pygdal=='$(gdalconfig --version).*'`
```sh
ogrmerge.py -o merged_streams.shp -t_srs "EPSG:3005" -single -progress wa_streams_clipped.shp bc_streams_clipped.shp 
```

Finally, burn the streams:
```sh
whitebox_tools -r=FillBurn -v --wd="./" --dem=srtm.tif --streams=merged_streams.shp -o=01_burned_srtm.tif
```

Create a COG:
```sh
gdal_translate "01_burned_srtm.tif" "Burned_SRTM_3005.tif" \
     -co TILED=YES -co BLOCKXSIZE=512 -co BLOCKYSIZE=512 \
     -co COMPRESS=LZW -co PREDICTOR=3 \
     -co COPY_SRC_OVERVIEWS=YES
```
Upload the resulting `Burned_SRTM_3005.tif` to Minio (staging and prod) and [create a fixture version](../../../fixtures/extents/README.md).


### Aspect

There are two aspect rasters to help us estimate the average aspect of a watershed.

Because we can't take the simple average of two angles (consider that the average of 350 and 10 is 180, but you would expect the average angle to be due north), we need to use a formula to calculate
the average aspect.

Start by creating an Aspect raster using WhiteBoxTools, and then create a raster for both the sine and cosine of the aspect value:

```sh
# transform to 3005
gdalwarp -t_srs EPSG:3005 -r cubic -of "GTiff" ./BC_Area_CDEM.tif ./01_dem_3005.tif 

# Create Aspect raster
whitebox_tools -r=Aspect -v --wd="$(pwd)" --dem=01_dem_3005.tif -o=02_aspect.tif 


# create sin and cos files
# https://www.perrygeo.com/average-aspect.html

gdal_calc.py -A 02_aspect.tif --calc "cos(radians(A))" --format "GTiff" --outfile 03_cos_aspect.tif
gdal_calc.py -A 02_aspect.tif --calc "sin(radians(A))" --format "GTiff" --outfile 03_sin_aspect.tif
```

Create the Cloud Optimized GeoTIFFs:
```sh
gdal_translate "03_cos_aspect.tif" "BC_Area_Aspect_COS_3005.tif" \
     -co TILED=YES -co BLOCKXSIZE=512 -co BLOCKYSIZE=512 \
     -co COMPRESS=LZW -co PREDICTOR=3 \
     -co COPY_SRC_OVERVIEWS=YES

gdal_translate "03_sin_aspect.tif" "BC_Area_Aspect_SIN_3005.tif" \
     -co TILED=YES -co BLOCKXSIZE=512 -co BLOCKYSIZE=512 \
     -co COMPRESS=LZW -co PREDICTOR=3 \
     -co COPY_SRC_OVERVIEWS=YES
```

To calculate aspect, collect the cos values and sin values in a polygon, and use them as
inputs to `math.atan2(sum(cos_values), sum(sin_values))`. This outputs an aspect in radians.
Credit: https://www.perrygeo.com/average-aspect.html

Note: some more research needs to be done to determine how accurate and useful this result is.

### Hillshade

Starting from a DEM (12 second) clipped to BC in BC Albers/3005, generate a new Hillshade raster:
```sh
whitebox_tools -r=HillShade -v --wd="$(pwd)" --dem=01_dem_3005.tif -o=04_hillshade.tif  --azimuth=180.0 --altitude=45.0
```

Create the COG:
```sh
gdal_translate "04_hillshade.tif" "BC_Area_Hillshade_3005.tif" \
     -co TILED=YES -co BLOCKXSIZE=512 -co BLOCKYSIZE=512 \
     -co COMPRESS=LZW -co PREDICTOR=2 \
     -co COPY_SRC_OVERVIEWS=YES
```