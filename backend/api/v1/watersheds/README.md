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
gdal_translate -of COG -co COMPRESS=LZW "01_burned.tif" "Burned_CDEM_4326.tif" \
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
gdal_translate -of COG "01_burned_srtm.tif" "Burned_SRTM_3005.tif" \
     -co COMPRESS=LZW 
```
Upload the resulting `Burned_SRTM_3005.tif` to Minio (staging and prod) and [create a fixture version](../../../fixtures/extents/README.md).


### Hillshade

Starting from a DEM (12 second) clipped to BC in BC Albers/3005, generate a new Hillshade raster:
```sh
whitebox_tools -r=HillShade -v --wd="$(pwd)" --dem=01_dem_3005.tif -o=04_hillshade.tif  --azimuth=180.0 --altitude=45.0
```

Create the COG:
```sh
gdal_translate -of COG -co COMPRESS=LZW "04_hillshade.tif" "BC_Area_Hillshade_3005.tif" \
     
```

### Climate rasters

The watershed statistics require the following datasets:

Climate WNA/PRISM data source:
Hamann, A. and Wang, T., Spittlehouse, D.L., and Murdock, T.Q. 2013. A comprehensive,
high-resolution database of historical and projected climate surfaces for western
North America. Bulletin of the American Meteorological Society 94: 1307–1309.
Retrieved from https://sites.ualberta.ca/~ahamann/data/climatewna.html on June 10, 2021

Potential evapotranspiration:
Trabucco, Antonio; Zomer, Robert (2019): Global Aridity Index and Potential
Evapotranspiration (ET0) Climate Database v2. figshare. Dataset.
https://doi.org/10.6084/m9.figshare.7504448.v3 
Retrieved from https://cgiarcsi.community/data/global-aridity-and-pet-database/ on June 10, 2021

#### Creating the COG tif files

Climate WNA precipitation:
1.  Download the annual bioclimate variables file
     (http://www.cacpd.org.s3.amazonaws.com/climate_normals/NORM_6190_Bioclim_ASCII.zip)

2.  Convert the MAP file (mean annual precipitation) to EPSG:4326:
     `gdalwarp -t_srs EPSG:4326 NORM_6190_MAP.tif precip.tif`

3.  Convert the resulting file to a COG:
     `gdal_translate -of COG -co COMPRESS=LZW precip.tif NORM_6190_Precip.tif`

4.  Upload the file to WALLY Staging and Prod Minio

Potential evapotranspiration:
1.  Download the database from the Global Aridity and PET link above. Unzip
     the file and then unzip the annual et0 file inside.

2.  Optional, but recommended:  use QGIS to get the extents of the above Climate WNA file,
     and clip the annual_et0.tif file.  The annual_et0.tif file has global coverage that we
     don't need.  Ensure the clipped area includes parts of Washington, Idaho, Alaska etc
     that BC watersheds originate in (e.g. Chilliwack River).

3.  Follow the instructions 2-4 for ClimateWNA to convert annual_et0.tif to EPSG:4326 and create a
     COG tif file named WNA_et0.tif.

Fixtures:
1.  Use the /backend/fixtures/extents file to clip Whistler area rasters for /backend/fixtures/raster.
