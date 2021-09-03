# Watersheds

Delineation of watersheds, summaries of watershed statistics, and aggregation of data pertaining to watersheds happens here.

For a high level overview of how the watershed delineation works, see [procedure.md](./procedure.md).

## Spatial rasters


WALLY uses a number of spatial raster files containing data to help delineate watersheds as well as extract information like
aspect and solar exposure. These files are converted to Cloud Optimized GeoTIFFs (COG) and stored in Minio. Using GDAL's COG
support, we can store large GeoTIFFs that cover the full province, and WALLY can request parts of the file by bounding box
coordinates.

### 12 arcsecond CDEM

The 12 arcsecond CDEM is used for simple statistics like average elevation and slope. It must be loaded into PostGIS. This file is NOT
used for watershed delineation.

* Download the file from https://ftp.maps.canada.ca/pub/nrcan_rncan/elevation/cdem_mnec/archive/ (cdem_12s.tif)
* Clip to an area around BC: 
```sh
gdalwarp -of "GTiff" -te -142 48 -112 62 ./cdem_12sec.tif ./BC_Area_CDEM.tif
```
* Store on Minio in the `raster` bucket.
* Use the import job `cdem.job.yaml` to import it to staging/production. See [the OCP4 migration README](../../../../openshift/ocp4/README.md) for detailed instructions.
* For local dev, a migration loads a Whistler area version. If you need to update it, look in the migrations.

### Preprocessed DEM with burned streams

Delineating watersheds requires a Digital Elevation Model (DEM) pre-processed to burn streams.  For watersheds in Canada, CDEM DEM data is used.
We also use the SRTM DEM along the border with Washington, Idaho and Montana. The SRTM-based DEM is automatically selected instead if the river
originates in the United States. Otherwise, the watershed delineation functions will select the best file for the area based on the files that
are registered in the `dem.stream_burned_cdem_tile` table.  

These DEMs are preprocessed for hydrological analysis and MUST NOT be used for elevation, slope or any other elevation data.

The current DEM files are:

**Burned_SRTM_3005.tif** - Automatically used for cross-border watersheds. Covers the 49th parallel. Projection: BC Albers (EPSG:3005) (note:
it is recommended that future DEMs use a consistent projection, either all 3005 or all 4326/lat lng.  This DEM requires a bunch of extra code
for transforming between 3005 and 4326)

**Burned_CDEM_4326.tif** - Province wide stream-burned coverage. This file is used if there is no 25m stream-burned coverage available in the selected area.

**Burned_SouthernBC_CDEM_25m.tif** - stream-burned 25m CDEM coverage for South Coast and Okanagan.

**Burned_WestCoast_CDEM_25m.tif** - stream-burned 25m CDEM coverage for Vancouver Island and most of the rest of the West Coast region.  Does not include Haida Gwaii (due to the large raster
size that would result).

**Burned_Caribou_CDEM_25m.tif** - stream-burned 25m CDEM coverage for the Caribou and Omineca regions and the rest of the northern mainland portion of the West Coast region.

All new 25m CDEM files must be loaded to Minio (staging and prod) and the extents must be registered in the `dem.stream_burned_cdem_tile` table. If done correctly,
the watershed delineation will automatically choose the new file, if it's the best file for the area.  The name of the file used is in the log output when using the Surface Water Analysis.


#### 3 arcsecond CDEM

The 3 arcsecond CDEM can provide province-wide coverage for watershed delineation in one file.  It must be stream-burned before use.
This file is located in Minio at `raster/Burned_CDEM_4326.tif`. The watershed delineation function will try to use higher res files where
available, but having this file available means there is always at least a low-resolution DEM for any area of the province.

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

#### 25m CDEM

The same procedure above is used for 25m CDEM, except that you first need to download individual tiles and stitch them together with `gdal_warp`. The
rest of the instructions apply.  Be sure to record the extents of the burned area as a shapefile and load it into the database - [see example](../../../alembic/versions/20210625150931_add_caribou_dem_extent.py).

https://ftp.maps.canada.ca/pub/nrcan_rncan/elevation/cdem_mnec/

The tiles correspond to the NTS Grid. Check https://www2.gov.bc.ca/gov/content/data/geographic-data-services/topographic-data/nts-base-map (or Google Images).

You may need at least 32 GB or more RAM to successfully burn an entire Natural Resource Region (e.g. Thompson Okanagan) using Whitebox Tools.
GRASS GIS, TauDEM and ArcGIS (ArcHydro) are alternatives that may require less RAM.

#### SRTM

SRTM tiles are available from EarthExplorer.
You will need the BC streams file from above and the Washington streams file from https://geo.wa.gov/datasets/71fa52e7d6224fde8b09facb12b30f04_24.

We use 3005 for SRTM DEM's, but we may want to refactor to 4326 in the future.

After downloading tiles for the desired area, merge the HGT format tiles together (**note**: EarthExplorer also offers compressed GeoTIFF files which may be a better option than HGT).
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
