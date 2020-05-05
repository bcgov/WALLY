# openshift/import-jobs

OpenShift jobs for data importing.  See `/imports/README.md` for more information.

# Downloading
hydrologic_zone_boundaries
## WFS Supported layers

These layers can be downloaded directly from the DataBC WFS API using the wfs scripts in `/imports`.
The `JOB_NAME` parameter is arbitrary but cannot contain underscores.

| Layer name (use as layer_name arg) | mapbox layer name | download job
| --- | --- | --- |
| water_rights_licenses                    | water_rights_licences | `oc process -f wfs.job.yaml -p JOB_NAME=licences -p LAYER_NAME=water_rights_licenses | oc apply -f -`
| ground_water_wells                       | groundwater_wells | `oc process -f wfs.job.yaml -p JOB_NAME=wells -p LAYER_NAME=ground_water_wells | oc apply -f -` 
(wells layer currently not working in Databc, manual download from GWELLS may be required)
| automated_snow_weather_station_locations | automated_snow_weather_station_locations | `oc process -f wfs.job.yaml -p JOB_NAME=snow -p LAYER_NAME=automated_snow_weather_station_locations | oc apply -f -`
| bc_wildfire_active_weather_stations      | bc_wildfire_active_weather_stations | `oc process -f wfs.job.yaml -p JOB_NAME=wildfire -p LAYER_NAME=bc_wildfire_active_weather_stations | oc apply -f -`
| ecocat_water_related_reports             | ecocat_water_related_reports | `oc process -f wfs.job.yaml -p JOB_NAME=ecocat -p LAYER_NAME=ecocat_water_related_reports | oc apply -f -`
| ground_water_aquifers                    | aquifers | `oc process -f wfs.job.yaml -p JOB_NAME=aquifers -p LAYER_NAME=ground_water_aquifers | oc apply -f -`
| hydrologic_zone_boundaries               | hydrologic_zone_boundaries | `oc process -f wfs.job.yaml -p JOB_NAME=hydrozones -p LAYER_NAME=hydrologic_zone_boundaries | oc apply -f -`
| water_rights_applications                | water_rights_applications | `oc process -f wfs.job.yaml -p JOB_NAME=applications -p LAYER_NAME=water_rights_applications | oc apply -f -`
| fn_community_locations                   | fn_community_locations | `oc process -f wfs.job.yaml -p JOB_NAME=fncommunities -p LAYER_NAME=fn_community_locations | oc apply -f -`
| fn_treaty_areas                          | fn_treaty_areas | `oc process -f wfs.job.yaml -p JOB_NAME=fntreatyareas -p LAYER_NAME=fn_treaty_areas | oc apply -f -`
| fn_treaty_lands                          | fn_treaty_lands | `oc process -f wfs.job.yaml -p JOB_NAME=fntreatylands -p LAYER_NAME=fn_treaty_lands | oc apply -f -`
| freshwater_atlas_glaciers                | freshwater_atlas_glaciers | `oc process -f wfs.job.yaml -p JOB_NAME=glaciers -p LAYER_NAME=freshwater_atlas_glaciers | oc apply -f -`
| water_approval_points                    | water_approval_points | `oc process -f wfs.job.yaml -p JOB_NAME=waterapprovalpoints -p LAYER_NAME=water_approval_points | oc apply -f -`

## Manual layers

The following layers must be manually downloaded, due to their large size.
Can also manually download layers from DataBC and then copy to minio server using `oc rsync ./local_dir/ <pod_name>:/remote_dir`
Copying to container only allows directory copy so best to isolate the file(s) you want to copy into their own directory.

| Layer name (use as layer_name arg) | mapbox layer name | download job
| --- | --- | --- |
| freshwater_atlas_watersheds              | freshwater_atlas_watersheds |    |
| bc_major_watersheds                      | bc_major_watersheds |    |
| cadastral                                | cadastral |    |
| freshwater_atlas_stream_directions       | freshwater_atlas_stream_directions |    |
| water_allocation_restrictions            | water_allocation_restrictions |    |
| critical_habitat_species_at_risk         | critical_habitat_species_at_risk |    |
| fish_observations                        | fish_observations |

### Hydat

Visit http://collaboration.cmc.ec.gc.ca/cmc/hydrometrics/www/ for the download link. New downloads are released quarterly. 

# Creating tiles

| Layer name (use as layer_name arg) | mapbox layer name | download job
| --- | --- | --- |
| aquifers                                 | aquifers | `oc process -f tippecanoe.job.yaml -p JOB_NAME=aquifers -p LAYER_NAME=aquifers | oc apply -f -`
| water_rights_licenses                    | water_rights_licences | `oc process -f tippecanoe.job.yaml -p JOB_NAME=licences -p LAYER_NAME=water_rights_licenses | oc apply -f -`
| ground_water_wells                       | groundwater_wells | `oc process -f tippecanoe.job.yaml -p JOB_NAME=wells -p LAYER_NAME=ground_water_wells | oc apply -f -`
| automated_snow_weather_station_locations | automated_snow_weather_station_locations | `oc process -f tippecanoe.job.yaml -p JOB_NAME=snow -p LAYER_NAME=automated_snow_weather_station_locations | oc apply -f -`
| bc_major_watersheds                      | bc_major_watersheds | `oc process -f tippecanoe.job.yaml -p JOB_NAME=bcmajorwatersheds -p LAYER_NAME=bc_major_watersheds | oc apply -f -`
| bc_wildfire_active_weather_stations      | bc_wildfire_active_weather_stations | `oc process -f tippecanoe.job.yaml -p JOB_NAME=wildfire -p LAYER_NAME=bc_wildfire_active_weather_stations | oc apply -f -`
| critical_habitat_species_at_risk         | critical_habitat_species_at_risk | `oc process -f tippecanoe.job.yaml -p JOB_NAME=criticalhabitat -p LAYER_NAME=critical_habitat_species_at_risk | oc apply -f -`
| ecocat_water_related_reports             | ecocat_water_related_reports | `oc process -f tippecanoe.job.yaml -p JOB_NAME=ecocat -p LAYER_NAME=ecocat_water_related_reports | oc apply -f -`
| ground_water_aquifers                    | aquifers | `oc process -f tippecanoe.job.yaml -p JOB_NAME=aquifers -p LAYER_NAME=ground_water_aquifers | oc apply -f -`
| hydrologic_zone_boundaries               | hydrologic_zone_boundaries | `oc process -f tippecanoe.job.yaml -p JOB_NAME=hydrozones -p LAYER_NAME=hydrologic_zone_boundaries | oc apply -f -`
| water_allocation_restrictions            | water_allocation_restrictions | unknown if supported (too many features) 
| critical_habitat_species_at_risk         | critical_habitat_species_at_risk | unknown if supported (too many features)
| water_rights_applications                | water_rights_applications | `oc process -f tippecanoe.job.yaml -p JOB_NAME=applications -p LAYER_NAME=water_rights_applications | oc apply -f -`
| fn_community_locations                   | fn_community_locations | `oc process -f tippecanoe.job.yaml -p JOB_NAME=fncommunities -p LAYER_NAME=fn_community_locations | oc apply -f -`
| fn_treaty_areas                          | fn_treaty_areas | `oc process -f tippecanoe.job.yaml -p JOB_NAME=fntreatyareas -p LAYER_NAME=fn_treaty_areas | oc apply -f -`
| fn_treaty_lands                          | fn_treaty_lands | `oc process -f tippecanoe.job.yaml -p JOB_NAME=fntreatylands -p LAYER_NAME=fn_treaty_lands | oc apply -f -`
| freshwater_atlas_glaciers                | freshwater_atlas_glaciers | `oc process -f tippecanoe.job.yaml -p JOB_NAME=glaciers -p LAYER_NAME=freshwater_atlas_glaciers | oc apply -f -`
| normal_annual_runoff_isolines            | normal_annual_runoff_isolines | `oc process -f tippecanoe.job.yaml -p JOB_NAME=isolines -p LAYER_NAME=normal_annual_runoff_isolines | oc apply -f -`
| fish_observations                        | fish_observations | `oc process -f tippecanoe.job.yaml -p JOB_NAME=fishobservations -p LAYER_NAME=fish_observations | oc apply -f -`
| water_approval_points                    | water_approval_points | `oc process -f tippecanoe.job.yaml -p JOB_NAME=waterapprovalpoints -p LAYER_NAME=water_approval_points | oc apply -f -`

## Freshwater Atlas

Freshwater Atlas layers are large and may need special options to process the layers into tiles.

### Stream networks

Break stream networks into 4 different chunks (zoom levels 0-4, 5-7, 8-10, and 11+).  The `STREAM_MAGNITUDE` property is used to filter out smaller streams/rivers when zoomed out.

See https://docs.mapbox.com/mapbox-gl-js/style-spec/#other-filter or https://www.github.com/mapbox/tippecanoe for documentation on filters.

```sh
tippecanoe -l freshwater_atlas_stream_networks  -j '
{
  "*": [
    "any",
    [
      "all",
      ["<=", "$zoom", 4],
      [">", "STREAM_MAGNITUDE", 700]
    ],
    [
      "all",
      [">", "$zoom", 4],
      ["<", "$zoom", 8],
      [">", "STREAM_MAGNITUDE", 300]
    ],
    [
      "all",
      [">=", "$zoom", 8],
      ["<=", "$zoom", 10],
      [">", "STREAM_MAGNITUDE", 20]
    ],
    [">", "$zoom", 10]
  ]
}' -z11 -o freshwater_atlas_stream_networks.mbtiles -y LINEAR_FEATURE_ID -y FWA_WATERSHED_CODE -y LOCAL_WATERSHED_CODE -y STREAM_MAGNITUDE -y DOWNSTREAM_ROUTE_MEASURE fwa_stream_networks.geojson
```

# Uploading tiles to Mapbox
Upload tiles to Mapbox by their mapbox source ID. This will gather all the `mbtiles` files that are associated with that source ID and upload them all together using tile-join.
| iit-water.first-nations                   | fn_community_locations, fn_treaty_areas, fn_treaty_lands | `oc process -f mapbox-upload.job.yaml -p JOB_NAME=first-nations -p LAYER_NAME=iit-water.first-nations | oc apply -f -`
| iit-water.0tsq064k                   | aquifers, bc_major_watersheds, critical_habitat_species_at_risk, freshwater_atlas_glaciers, hydrologic_zone_boundaries, normal_annual_runoff_isolines | `oc process -f mapbox-upload.job.yaml -p JOB_NAME=0tsq064k -p LAYER_NAME=iit-water.0tsq064k | oc apply -f -`
| iit-water.448thhpa                   | water_rights_licences, fish_observations, water_approval_points | `oc process -f mapbox-upload.job.yaml -p JOB_NAME=448thhpa -p LAYER_NAME=iit-water.448thhpa | oc apply -f -`

# Importing into the Wally database

| Layer name (use as layer_name arg) | mapbox layer name | download job
| --- | --- | --- |
| water_rights_applications                | water_rights_applications | `oc process -f import.job.yaml -p JOB_NAME=applications -p LAYER_NAME=water_rights_applications | oc apply -f -`
| water_rights_licenses                    | water_rights_licenses | `oc process -f import.job.yaml -p JOB_NAME=licences -p LAYER_NAME=water_rights_licenses | oc apply -f -`
| ground_water_wells                       | groundwater_wells | `oc process -f import.job.yaml -p JOB_NAME=wells -p LAYER_NAME=ground_water_wells | oc apply -f -`
| automated_snow_weather_station_locations | automated_snow_weather_station_locations | `oc process -f import.job.yaml -p JOB_NAME=snow -p LAYER_NAME=automated_snow_weather_station_locations | oc apply -f -`
| bc_wildfire_active_weather_stations      | bc_wildfire_active_weather_stations | `oc process -f import.job.yaml -p JOB_NAME=wildfire -p LAYER_NAME=bc_wildfire_active_weather_stations | oc apply -f -`
| ecocat_water_related_reports             | ecocat_water_related_reports | `oc process -f import.job.yaml -p JOB_NAME=ecocat -p LAYER_NAME=ecocat_water_related_reports | oc apply -f -`
| ground_water_aquifers                    | aquifers | `oc process -f import.job.yaml -p JOB_NAME=aquifers -p LAYER_NAME=ground_water_aquifers | oc apply -f -`
| fn_community_locations                   | fn_community_locations | `oc process -f import.job.yaml -p JOB_NAME=fncommunities -p LAYER_NAME=fn_community_locations | oc apply -f -`
| fn_treaty_areas                          | fn_treaty_areas | `oc process -f import.job.yaml -p JOB_NAME=fntreatyareas -p LAYER_NAME=fn_treaty_areas | oc apply -f -`
| fn_treaty_lands                          | fn_treaty_lands | `oc process -f import.job.yaml -p JOB_NAME=fntreatylands -p LAYER_NAME=fn_treaty_lands | oc apply -f -`
| normal_annual_runoff_isolines            | normal_annual_runoff_isolines | `oc process -f import.job.yaml -p JOB_NAME=isolines -p LAYER_NAME=normal_annual_runoff_isolines | oc apply -f -`


# Cron jobs setup and management

- Helpful commands

`oc get jobs` to see run jobs history
`oc get cronjobs` to see currently scheduled cronjobs
`oc delete cronjob/<cron_job_name>` delete cronjob

## Start WFS download cron jobs which pull data from DataBC 

- These download jobs run nightly between 2am-3am - 5 minutes apart

| water_rights_licenses                     | `oc process -f wfs.cron.job.yaml -p SCHEDULE_TIME="0 2 * * *" -p JOB_NAME=licences -p LAYER_NAME=water_rights_licenses | oc apply -f -`
| automated_snow_weather_station_locations  | `oc process -f wfs.cron.job.yaml -p SCHEDULE_TIME="5 2 * * *" -p JOB_NAME=snowstations -p LAYER_NAME=automated_snow_weather_station_locations | oc apply -f -`
| bc_wildfire_active_weather_stations       | `oc process -f wfs.cron.job.yaml -p SCHEDULE_TIME="10 2 * * *" -p JOB_NAME=firestations -p LAYER_NAME=bc_wildfire_active_weather_stations | oc apply -f -`
| ecocat_water_related_reports              | `oc process -f wfs.cron.job.yaml -p SCHEDULE_TIME="15 2 * * *" -p JOB_NAME=ecocat -p LAYER_NAME=ecocat_water_related_reports | oc apply -f -`
| ground_water_aquifers                     | `oc process -f wfs.cron.job.yaml -p SCHEDULE_TIME="20 2 * * *" -p JOB_NAME=aquifers -p LAYER_NAME=ground_water_aquifers | oc apply -f -`
| water_rights_applications                 | `oc process -f wfs.cron.job.yaml -p SCHEDULE_TIME="25 2 * * *" -p JOB_NAME=applications -p LAYER_NAME=water_rights_applications | oc apply -f -`
| fn_community_locations                    | `oc process -f wfs.cron.job.yaml -p SCHEDULE_TIME="30 2 * * *" -p JOB_NAME=fncommunities -p LAYER_NAME=fn_community_locations | oc apply -f -`
| fn_treaty_areas                           | `oc process -f wfs.cron.job.yaml -p SCHEDULE_TIME="35 2 * * *" -p JOB_NAME=fntreatyareas -p LAYER_NAME=fn_treaty_areas | oc apply -f -`
| fn_treaty_lands                           | `oc process -f wfs.cron.job.yaml -p SCHEDULE_TIME="40 2 * * *" -p JOB_NAME=fntreatylands -p LAYER_NAME=fn_treaty_lands | oc apply -f -`
| freshwater_atlas_glaciers                 | `oc process -f wfs.cron.job.yaml -p SCHEDULE_TIME="45 2 * * *" -p JOB_NAME=glaciers -p LAYER_NAME=freshwater_atlas_glaciers | oc apply -f -`
| water_approval_points                     | `oc process -f wfs.cron.job.yaml -p SCHEDULE_TIME="50 2 * * *" -p JOB_NAME=waterapprovalpoints -p LAYER_NAME=water_approval_points | oc apply -f -`

## Manual <layername>.zip placement required in prod Minio data/geojson folder

| freshwater_atlas_watersheds
| bc_major_watersheds
| cadastral
| freshwater_atlas_stream_directions
| water_allocation_restrictions
| critical_habitat_species_at_risk
| fish_observations

## Start vector tile creation cron jobs

- These tile jobs run nightly between 3am-4:30am - 5 minutes apart

| water_rights_licenses                     | `oc process -f tippecanoe.cron.job.yaml -p SCHEDULE_TIME="0 3 * * *" -p JOB_NAME=licences -p LAYER_NAME=water_rights_licenses | oc apply -f -`
| automated_snow_weather_station_locations  | `oc process -f tippecanoe.cron.job.yaml -p SCHEDULE_TIME="5 3 * * *" -p JOB_NAME=snowstations -p LAYER_NAME=automated_snow_weather_station_locations | oc apply -f -`
| bc_wildfire_active_weather_stations       | `oc process -f tippecanoe.cron.job.yaml -p SCHEDULE_TIME="10 3 * * *" -p JOB_NAME=firestations -p LAYER_NAME=bc_wildfire_active_weather_stations | oc apply -f -`
| ecocat_water_related_reports              | `oc process -f tippecanoe.cron.job.yaml -p SCHEDULE_TIME="15 3 * * *" -p JOB_NAME=ecocat -p LAYER_NAME=ecocat_water_related_reports | oc apply -f -`
| ground_water_aquifers                     | `oc process -f tippecanoe.cron.job.yaml -p SCHEDULE_TIME="20 3 * * *" -p JOB_NAME=aquifers -p LAYER_NAME=ground_water_aquifers | oc apply -f -`
| water_rights_applications                 | `oc process -f tippecanoe.cron.job.yaml -p SCHEDULE_TIME="25 3 * * *" -p JOB_NAME=applications -p LAYER_NAME=water_rights_applications | oc apply -f -`
| fn_community_locations                    | `oc process -f tippecanoe.cron.job.yaml -p SCHEDULE_TIME="30 3 * * *" -p JOB_NAME=fncommunities -p LAYER_NAME=fn_community_locations | oc apply -f -`
| fn_treaty_areas                           | `oc process -f tippecanoe.cron.job.yaml -p SCHEDULE_TIME="35 3 * * *" -p JOB_NAME=fntreatyareas -p LAYER_NAME=fn_treaty_areas | oc apply -f -`
| fn_treaty_lands                           | `oc process -f tippecanoe.cron.job.yaml -p SCHEDULE_TIME="40 3 * * *" -p JOB_NAME=fntreatylands -p LAYER_NAME=fn_treaty_lands | oc apply -f -`
| freshwater_atlas_glaciers                 | `oc process -f tippecanoe.cron.job.yaml -p SCHEDULE_TIME="45 3 * * *" -p JOB_NAME=glaciers -p LAYER_NAME=freshwater_atlas_glaciers | oc apply -f -`
| water_approval_points                     | `oc process -f tippecanoe.cron.job.yaml -p SCHEDULE_TIME="50 3 * * *" -p JOB_NAME=waterapprovalpoints -p LAYER_NAME=water_approval_points | oc apply -f -`

- Manual upload required so may not want to auto run these
| cadastral                                 | `oc process -f tippecanoe.cron.job.yaml -p SCHEDULE_TIME="55 3 * * *" -p JOB_NAME=cadastral -p LAYER_NAME=cadastral | oc apply -f -`
| fish_observations                         | `oc process -f tippecanoe.cron.job.yaml -p SCHEDULE_TIME="0 4 * * *" -p JOB_NAME=fishobservations -p LAYER_NAME=fish_observations | oc apply -f -`
| water_allocation_restrictions             | `oc process -f tippecanoe.cron.job.yaml -p SCHEDULE_TIME="5 4 * * *" -p JOB_NAME=allocationrestrictions -p LAYER_NAME=water_allocation_restrictions | oc apply -f -`
| critical_habitat_species_at_risk          | `oc process -f tippecanoe.cron.job.yaml -p SCHEDULE_TIME="10 4 * * *" -p JOB_NAME=criticalhabitat -p LAYER_NAME=critical_habitat_species_at_risk | oc apply -f -`

## Start Mapbox layer upload cron jobs

- These upload jobs run nightly between 4:30am-5:00am - 5 minutes apart

| iit-water.first-nations   | fn_community_locations, fn_treaty_areas, fn_treaty_lands | `oc process -f mapbox-upload.cron.job.yaml -p SCHEDULE_TIME="30 4 * * *" -p JOB_NAME=first-nations -p LAYER_NAME=iit-water.first-nations | oc apply -f -`
| iit-water.0tsq064k        | aquifers, bc_major_watersheds, critical_habitat_species_at_risk, freshwater_atlas_glaciers, hydrologic_zone_boundaries, normal_annual_runoff_isolines | `oc process -f mapbox-upload.cron.job.yaml -p SCHEDULE_TIME="35 4 * * *" -p JOB_NAME=0tsq064k -p LAYER_NAME=iit-water.0tsq064k | oc apply -f -`
| iit-water.448thhpa        | water_rights_licences, fish_observations, water_approval_points | `oc process -f mapbox-upload.cron.job.yaml -p SCHEDULE_TIME="40 4 * * *" -p JOB_NAME=448thhpa -p LAYER_NAME=iit-water.448thhpa | oc apply -f -`
| iit-water.36r1x37x        | cadastral | `oc process -f mapbox-upload.cron.job.yaml -p SCHEDULE_TIME="45 4 * * *" -p JOB_NAME=36r1x37x -p LAYER_NAME=iit-water.36r1x37x | oc apply -f -`
| iit-water.2svbut5f        | automated_snow_weather_station_locations, bc_wildfire_active_weather_stations, ecocat_water_related_reports, water_rights_applications, groundwater_wells | `oc process -f mapbox-upload.cron.job.yaml -p SCHEDULE_TIME="50 4 * * *" -p JOB_NAME=2svbut5f -p LAYER_NAME=iit-water.2svbut5f | oc apply -f -`

### Manual tile creation and upload to Mapbox
- These layers don't change much so should probably only be updated annually using the manual run jobs
| freshwater_atlas_stream_networks | iit-water.6q8q0qac
| freshwater_atlas_stream_directions | iit-water.56s6dyhu
| freshwater_atlas_watersheds | iit-water.7iwr3fo1
| bc_major_watersheds | iit-water.0tsq064k (currently lives in an auto-updated nightly layer)
| hydrologic_zone_boundaries | iit-water.0tsq064k (currently lives in an auto-updated nightly layer)
| normal_annual_runoff_isolines | this is a manual layer that was created and imported into the wally database which probably never needs to be updated because its based on historical data

### Hydat hydrometric_stream_flow layer
Source should be checked monthly for new data from http://collaboration.cmc.ec.gc.ca/cmc/hydrometrics/www/
then convert sql data to geojson.zip and place in data/geojson folder on prod Minio
import data into prod database 
and then run the manual tile creation and upload jobs to Mapbox layer iit-water.31epl7h1
