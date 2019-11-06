# Data loading tools

Tools for downloading GeoJSON format layer data from DataBC or other external sources and loading it into Wally

**Note**:

All references to `layer_name` mean the database table name for the layer. Check the `__tablename__` attribute
in the files in wally/backend/app/layers.  `<layer_name>.zip` will be used as a filename for storing the downloaded files and then for retrieving them later by the ogr2ogr or tippecanoe jobs.

The Mapbox vector tile layer names may not necessarily be the same as the `layer_name` referred to in this readme and the tools in this folder.  The Mapbox vector tile layer name can be looked up using the `metadata.display_catalogue` database table.
DataBC also has their own names for each dataset, which can be found in `metadata.data_source`.
A future task should be to make the names as consistent as possible.

The OpenShift jobs for these steps are located in `/openshift/import-jobs`.

## Workflow

### 1. Downloading data
#### Small datasets

For datasets with fewer than ~100,000 records, data can be scraped directly from DataBC WFS using `wfs_direct_download.sh <layer_name>` (OpenShift job: `wfs.job.yaml`). More than 100,000 records will require >10 requests to complete (requests are automatically made until data is completely downloaded); proceed at own risk. The following datasets are
close to 100,000 or fewer:

* ground_water_aquifers
* ground_water_wells
* water_rights_licenses
* automated_snow_weather_station_locations
* ecocat_water_related_reports
* critical_habitat_species_at_risk

#### Large datasets

Larger datasets should be downloaded from DataBC API Catalogue.  At the moment, the only way is to make a request at the DataBC catalogue using your email address.  The link will be emailed to you.  You can either load the zip file directly (important: the zip file should contain only ONE dataset) onto Wally's Minio service, or you can use `download_layer.sh <table_name> <link>`  (OpenShift job: download.job.yaml).
A future task should be to make a request automatically and then monitor the OFI service (https://catalogue.data.gov.bc.ca/dataset/data-download-order-fulfiller-interface-dwds-ofi-) for the download
to become available.  Once this is automated, the download link can be fed into `download_layer.sh <layer_name> <link>`.

#### Hydat (Federal Government)

Hydat is not a DataBC layer, and the tools in this folder will not work. See the `./hydat` folder.

### 2. Loading data

DataBC geojson data is loaded using ogr2ogr. Once a zipped geojson file is available on s3 storage (which should have happened if using either `wfs_direct_download.sh` or `download_layer.sh`), use `load_layer_data.sh` (job: import.job.yaml).  This script will run ogr2ogr on the zipped geojson file, and will then update the `metadata.data_source` table to indicate that the data was updated. **Important:** the updated date is taken from the "last modified" value of the source geojson file, and NOT the time when the load script was run. This is to prevent
data from being reported as recently updated if the script was run on stale data (for whatever reason).

### 3. Generating Mapbox vector tiles

The tiles folder contains a script for generating tiles: `./create_tileset.sh <layer_name>`.  This script will create an mbtiles file (Mapbox vector tiles) out of a geojson file (stored in Minio/S3 storage) for the layer_name given.  This step depends upon data downloaded in step 1.  The data should match the data loaded in the database (step 2), but these steps can be run in any order or at the same time.

The output of `create_tileset.sh` is a `layer_name.mbtiles` file in the mbtiles bucket of the Minio storage.

### 4. Uploading vector tiles to the Mapbox service

To be completed...

## Future steps/improvements

All scripts in this folder have a corresponding OpenShift/k8s job template (*.job.yaml).  These jobs can be run in sequence (download data, load data, etc) by a task runner or just scheduled as cronjobs.

The scripts make psql commands to get metadata and update "last_updated" type columns, and load data into tables using ogr2ogr.  This means these jobs/tools could be impacted by database changes by the backend API (`wally/backend`).  This includes tables defined in `wally/backend/app/layers` and `/wally/backend/app/metadata`.