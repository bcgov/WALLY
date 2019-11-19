# openshift/import-jobs

OpenShift jobs for data importing.  See `/imports/README.md` for more information.

# Downloading

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
| water_allocation_restrictions            | water_allocation_restrictions | unknown if supported (too many features) 
| critical_habitat_species_at_risk         | critical_habitat_species_at_risk | unknown if supported (too many features)
| water_rights_applications                | water_rights_applications | `oc process -f wfs.job.yaml -p JOB_NAME=applications -p LAYER_NAME=water_rights_applications | oc apply -f -`

## Manual layers

The following layers must be manually downloaded, due to their large size.

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
| water_rights_licenses                    | water_rights_licences | `oc process -f tippecanoe.job.yaml -p JOB_NAME=licences -p LAYER_NAME=water_rights_licenses | oc apply -f -`
| ground_water_wells                       | groundwater_wells | `oc process -f tippecanoe.job.yaml -p JOB_NAME=wells -p LAYER_NAME=ground_water_wells | oc apply -f -`
| automated_snow_weather_station_locations | automated_snow_weather_station_locations | `oc process -f tippecanoe.job.yaml -p JOB_NAME=snow -p LAYER_NAME=automated_snow_weather_station_locations | oc apply -f -`
| bc_wildfire_active_weather_stations      | bc_wildfire_active_weather_stations | `oc process -f tippecanoe.job.yaml -p JOB_NAME=wildfire -p LAYER_NAME=bc_wildfire_active_weather_stations | oc apply -f -`
| ecocat_water_related_reports             | ecocat_water_related_reports | `oc process -f tippecanoe.job.yaml -p JOB_NAME=ecocat -p LAYER_NAME=ecocat_water_related_reports | oc apply -f -`
| ground_water_aquifers                    | aquifers | `oc process -f tippecanoe.job.yaml -p JOB_NAME=aquifers -p LAYER_NAME=ground_water_aquifers | oc apply -f -`
| water_allocation_restrictions            | water_allocation_restrictions | unknown if supported (too many features) 
| critical_habitat_species_at_risk         | critical_habitat_species_at_risk | unknown if supported (too many features)
| water_rights_applications                | water_rights_applications | `oc process -f tippecanoe.job.yaml -p JOB_NAME=applications -p LAYER_NAME=water_rights_applications | oc apply -f -`

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
}' -z11 -o freshwater_atlas_stream_networks.mbtiles -y LINEAR_FEATURE_ID -y FWA_WATERSHED_CODE -y LOCAL_WATERSHED_CODE -y STREAM_MAGNITUDE -y DOWNSTREAM_ROUTE_MEASURE fwa_stream_networks.geojson```



# Importing into the Wally database

| Layer name (use as layer_name arg) | mapbox layer name | download job
| --- | --- | --- |
| water_rights_applications                    | water_rights_licences | `oc process -f import.job.yaml -p JOB_NAME=applications -p LAYER_NAME=water_rights_applications | oc apply -f -`
