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
| automated_snow_weather_station_locations | automated_snow_weather_station_locations | `oc process -f wfs.job.yaml -p JOB_NAME=snow -p LAYER_NAME=automated_snow_weather_station_locations | oc apply -f -`
| bc_wildfire_active_weather_stations      | bc_wildfire_active_weather_stations | `oc process -f wfs.job.yaml -p JOB_NAME=wildfire -p LAYER_NAME=bc_wildfire_active_weather_stations | oc apply -f -`
| ecocat_water_related_reports             | ecocat_water_related_reports | `oc process -f wfs.job.yaml -p JOB_NAME=ecocat -p LAYER_NAME=ecocat_water_related_reports | oc apply -f -`
| ground_water_aquifers                    | aquifers | `oc process -f wfs.job.yaml -p JOB_NAME=aquifers -p LAYER_NAME=ground_water_aquifers | oc apply -f -`
| hydrologic_zone_boundaries               | hydrologic_zone_boundaries | `oc process -f wfs.job.yaml -p JOB_NAME=hydrozones -p LAYER_NAME=hydrologic_zone_boundaries | oc apply -f -`
| water_allocation_restrictions            | water_allocation_restrictions | unknown if supported (too many features) 
| critical_habitat_species_at_risk         | critical_habitat_species_at_risk | unknown if supported (too many features)
| water_rights_applications                | water_rights_applications | `oc process -f wfs.job.yaml -p JOB_NAME=applications -p LAYER_NAME=water_rights_applications | oc apply -f -`
| fn_community_locations                   | fn_community_locations | `oc process -f wfs.job.yaml -p JOB_NAME=fncommunities -p LAYER_NAME=fn_community_locations | oc apply -f -`
| fn_treaty_areas                          | fn_treaty_areas | `oc process -f wfs.job.yaml -p JOB_NAME=fntreatyareas -p LAYER_NAME=fn_treaty_areas | oc apply -f -`
| fn_treaty_lands                          | fn_treaty_lands | `oc process -f wfs.job.yaml -p JOB_NAME=fntreatylands -p LAYER_NAME=fn_treaty_lands | oc apply -f -`
| freshwater_atlas_glaciers                | freshwater_atlas_glaciers | `oc process -f wfs.job.yaml -p JOB_NAME=glaciers -p LAYER_NAME=freshwater_atlas_glaciers | oc apply -f -`

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
| freshwater_atlas_glaciers                | freshwater_atlas_glaciers | `oc process -f tippecanoe.job.yaml -p JOB_NAME=glaciers -p LAYER_NAME=freshwater_atlas_glaciers | oc apply -f -`
| normal_annual_runoff_isolines            | normal_annual_runoff_isolines | `oc process -f tippecanoe.job.yaml -p JOB_NAME=isolines -p LAYER_NAME=normal_annual_runoff_isolines | oc apply -f -`

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

