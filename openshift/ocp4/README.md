# Migrating from OCP3 to OCP4

Note: These are the steps required to stand up WALLY on a new platform environment. The instructions are for an OpenShift multitenant platform
with 4 namespaces:  `<project_id>-tools`, `<project_id>-dev`, `<project_id>-test` and `<project_id>-prod`.  Supporting services like Jenkins
as well as all the build resources and secrets for pulling from GitHub and container registries go in the Tools namespace.

# Prerequisites for TOOLS/DEV/TEST/PROD namespaces

Note for migrating: Most resources that need to be created in the environments but are not stored in templates in the repo (such as secrets) can be retrieved from OCP3 using `oc get secret wally-at-github -o yaml`.

## Create or import secrets/configmaps

### Tools namespace
#### Secrets
* wally-at-github (GitHub SSH key)
* wally-github-token (GitHub token)
* apitest-test-creds (test account for CI/CD API tests)

### Dev namespace
#### Secrets
* common-docgen
* wally-psql
* minio
* keycloak-config
* gatekeeper-credentials
* wally-debug
* mapbox-access-token

#### ConfigMaps
* gatekeeper-config
* promtail-config
* loki-config
* wally-config


### Test

#### Secrets
* common-docgen
* wally-psql
* minio
* gatekeeper-credentials
* wally-debug
* mapbox-access-token

#### ConfigMaps
* gatekeeper-config
* promtail-config
* loki-config
* wally-config
* wally-staging-grafana
* wally-staging-grafana-cfg
* wally-staging-grafana-dashboards
* wally-staging-grafana-datasources
* wally-grafana-notifiers
* wally-staging-prometheus
* apitest-monitors

### Prod

#### Secrets
* common-docgen
* wally-psql
* minio
* gatekeeper-credentials
* wally-debug
* mapbox-access-token

#### ConfigMaps
* gatekeeper-config
* promtail-config
* loki-config
* wally-config
* wally-grafana
* wally-grafana-cfg
* wally-grafana-dashboards
* wally-grafana-datasources
* wally-grafana-notifiers
* wally-prometheus
* apitest-monitors

## Import images

The following external/community images don't have BuildConfigs and need to be imported:
Example import command: `oc4 -n d1b5d2-tools import-image --from=python:3.7 python:3.7 --reference-policy=local --confirm`

Note: see https://github.com/BCDevOps/OpenShift4-Migration/issues/51.  With Artifactory credentials the `--from=python:3.7` above can be replaced
with `--from=docker-remote.artifacts.developer.gov.bc.ca`

* `python:3.7`
* `crunchy-postgres-gis:centos7-12.5-3.0-4.4.2` - note: this image was not used for Wally on OpenShift 3. It's new for OCP4.  Database templates for this new image are in openshift/ocp4/crunchy-postgres .
* `promtail:v1.3.0` - Log exporter for Loki
* `apitest` - Warning: technical debt: this image needs a BuildConfig to be built using source code from github.com/stephenhillier/apitest onto a Red Hat Jenkins agent image.  The current image was transferred from OCP3.

Refer to https://github.com/BCDevOps/OpenShift4-Migration/issues/51 for instructions on how to enable pull secrets for builds using Docker Hub images.

## Set up NetworkPolicy

* there is a quickstart set of NetworkPolicies, see `quickstart-network-policy.yaml`. Must be applied to each namespace.
* TODO: set finer grained rules.

## Create BuildConfigs

The core application BuildConfigs will be created by Jenkins (see the Jenkinsfile).  Some supporting BuildConfigs need to be created manually once when deploying
to a new platform environment.

* `openshift/import-jobs/importer.build.yaml` - this allows using the jobs in `openshift/import-jobs` to populate the database.

## Upload data required by Wally

Wally requires data from the Freshwater Atlas, PRISM, Hydat (Water Survey of Canada database), and the 12 arcsecond CDEM.

These files need to be uploaded to Minio:
```
/geojson/freshwater_atlas_watersheds.zip
/geojson/freshwater_atlas_stream_networks.zip
/raster/prism_pr.asc
/raster/prism_pr.prj
/raster/BC_Area_CDEM.tif
```

`freshwater_atlas_watersheds.zip` - Freshwater Atlas Watersheds:
* Download from the GeoBC ftp site: `ftp://ftp.gdbc.gov.bc.ca/sections/outgoing/bmgs/FWA_Public/FWA_WATERSHEDS_POLY.gdb/`
* Rename to `freshwater_atlas_watersheds.gdb/`.  This step helps the script match the file to the WALLY database table "freshwater_atlas_watersheds".
* zip: `zip -r freshwater_atlas_watersheds freshwater_atlas_watersheds.gdb`
* Upload to the `geojson` bucket.  This isn't a geojson file, but the bucket for data dumps was previously named geojson. TODO: rename to a more general name.

`freshwater_atlas_stream_networks.zip` - Freshwater Atlas Stream Networks:
* Download from `ftp://ftp.gdbc.gov.bc.ca/sections/outgoing/bmgs/FWA_Public/FWA_STREAM_NETWORKS_SP.gdb/`
* rename to `freshwater_atlas_stream_networks.gdb` and zip
* follow rest of instructions as above.

`prism_pr.asc` and `prism_pr.prj` - PRISM precipitation.
* Download from Pacific Climate Impacts Consortium
* upload to the `raster` bucket.

`BC_Area_CDEM.tif`:
* Download from `https://ftp.maps.canada.ca/pub/nrcan_rncan/elevation/cdem_mnec/archive/`.
* 12 second is sufficient for the functions that use the DEM directly
* Reproject to EPSG:4326 and crop to approximate BC area (TODO: add a command e.g. `gdalwarp -t_srs EPSG:4326 -te <xmin ymin xmax ymax> cdem.tif`).
* Ensure that enough of Alberta, NWT, Yukon are included since some watersheds originate outside BC. (TODO: confirm bounds required to not clip any watersheds that drain to BC)


## Populate databases

The following needs to be done for both staging and prod.


### Layer data

Most layer data (e.g. point of interest, polygon search etc) pull directly from DataBC except for the following
* First Nations treaty areas
* First Nations communities
* First Nations treaty lands


```sh
# job to automatically download and store on Minio
oc process -f wfs.job.yaml -p JOB_NAME=fncommunities -p MINIO_HOST_URL=http://wally-minio-staging:9000 -p LAYER_NAME=fn_community_locations | oc apply -f -
oc process -f wfs.job.yaml -p JOB_NAME=fntreatyareas -p MINIO_HOST_URL=http://wally-minio-staging:9000 -p LAYER_NAME=fn_treaty_areas | oc apply -f -
oc process -f wfs.job.yaml -p JOB_NAME=fntreatylands -p MINIO_HOST_URL=http://wally-minio-staging:9000 -p LAYER_NAME=fn_treaty_lands | oc apply -f -

# job to load into Postgres
oc process -f import.job.yaml -p JOB_NAME=fncommunities -p MINIO_HOST_URL=http://wally-minio-staging:9000 -p LAYER_NAME=fn_community_locations | oc apply -f -
oc process -f import.job.yaml -p JOB_NAME=fntreatyareas -p MINIO_HOST_URL=http://wally-minio-staging:9000 -p LAYER_NAME=fn_treaty_areas | oc apply -f -
oc process -f import.job.yaml -p JOB_NAME=fntreatylands -p MINIO_HOST_URL=http://wally-minio-staging:9000 -p LAYER_NAME=fn_treaty_lands | oc apply -f -
```

### Freshwater Atlas
Freshwater Atlas watersheds and stream networks need to be loaded. This takes time (possibly several hours).

**Warning:**
Loading data will create very large log files in `/pgdata/userdata/pg_log`. They can/should be removed.
Be careful that they don't fill up the disk.
TODO:  investigate turning down statement logging while loading data.

```sh
# fwa watersheds
# requires freshwater_atlas_watersheds.zip (containing freshwater_atlas_watersheds.gdb). See above for instructions.
oc process -f import.job.yaml -p JOB_NAME=watersheds -p ENV_NAME=staging -p LAYER_NAME=freshwater_atlas_watersheds \
   -p SCRIPT_PATH=/dataload/load_fwa.sh -p MINIO_HOST_URL=http://wally-minio-staging:9000 | oc apply -f -

# fwa stream networks
# requires freshwater_atlas_stream_networks.zip (containing freshwater_atlas_stream_networks.gdb).  See above.
oc process -f import.job.yaml -p JOB_NAME=streams -p ENV_NAME=staging -p LAYER_NAME=freshwater_atlas_stream_networks \
 -p SCRIPT_PATH=/dataload/load_fwa.sh -p MINIO_HOST_URL=http://wally-minio-staging:9000 | oc4 apply -f -
```

### Raster data

```sh
# prism
# requires raster/prism_pr.asc and raster/prism_pr.prj in Minio storage
oc4 process -f prism.job.yaml -p ENV_NAME=staging -p MINIO_HOST_URL=http://wally-minio-staging:9000  | oc apply -f -

# CDEM
# requires raster/BC_Area_CDEM.tif in Minio storage
oc4 process -f cdem.job.yaml -p ENV_NAME=staging -p MINIO_HOST_URL=http://wally-minio-staging:9000 | oc apply -f -

# Hydat
# downloads its own data, but the link has to be updated for new HYDAT versions (approximately quarterly). See wally/imports/hydat/load_hydat.sh
oc4 process -f hydat.job.yaml -p ENV_NAME=staging | oc apply -f -
```

### Prod data
This is an abbreviated version of the above for PROD.  Refer to the above for instructions. The same files need
to be on Minio in the prod namespace.
```sh
oc process -f import.job.yaml -p JOB_NAME=watersheds -p ENV_NAME=production -p LAYER_NAME=freshwater_atlas_watersheds \
   -p SCRIPT_PATH=/dataload/load_fwa.sh -p MINIO_HOST_URL=http://wally-minio-production:9000 | oc apply -f -

oc process -f import.job.yaml -p JOB_NAME=streams -p ENV_NAME=production -p LAYER_NAME=freshwater_atlas_stream_networks \
 -p SCRIPT_PATH=/dataload/load_fwa.sh -p MINIO_HOST_URL=http://wally-minio-production:9000 | oc4 apply -f -

oc4 process -f prism.job.yaml -p ENV_NAME=production -p MINIO_HOST_URL=http://wally-minio-production:9000  | oc apply -f -
oc4 process -f cdem.job.yaml -p ENV_NAME=production -p MINIO_HOST_URL=http://wally-minio-production:9000 | oc apply -f -
oc4 process -f hydat.job.yaml -p ENV_NAME=production | oc apply -f -

```
