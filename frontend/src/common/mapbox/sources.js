/*
Historical sources used in the development style on MapBox studio:
iit-water.56s6dyhu - wally_freshwater_atlas_stream-6ml1n5
iit-water.9jyty6rt - groundwater_wells_subset-8rbrc9
iit-water.2xk41k05 - water_rights_applications-9zhw62
iit-water.8rt7ts1c - glaciers_and_isolines-28fnv1
iit-water.0r2u1e4m - wally_testing_whistler_subset-5da6z2
iit-water.bf1gc2mz - hydat-879a50
iit-water.6ihj1ke0 - FWA_STREAM_NETWORKS_SP-bdhkfq
iit-water.2ah76e1a - stream_restrictions-5qgetu
iit-water.first-nations-subset
iit-water.7804omec - critical_habitat_species_at_r-cy8usw
iit-water.7iwr3fo1 - pk_freshwater_atlas_watershed-cem099

glaciers_and_isolines-28fnv1
- fish_obstacles
- water_approval_points
- fish_observations
- fish_observations_summary
- normal_annual_isolines
- freshwater_atlas_glaciers
- water_licenced_works
- water_licenced_works_dash1
- water_licenced_works_dash2
- water_licenced_works_dash3
- water_licenced_works_dash4

first-nations-subset
- fn_treaty_lands
- fn_treaty_areas
- fn_community_locations

FWA_STREAM_NETWORKS_SP-bdhkfq
- freshwater_atlast_stream_networks

water_rights_applications-9zhw62
- water_rights_applications

groundwater_wells_subset-8rbrc9
- groundwater_wells

wally_testing_whistler_subset-5da6z2
- water_rights_licences
- automated_snow_weather_stations
- bc_wildfire_active_weather_stations
- ecocat_water_related_report
- bc_major_watershedss
- cadastral
- aquifers

hydat-879a50
- hydrometric_stream_flow

critical_habitat_species_at_r-cy8usw
- critical_habitat_species

wally_freshwater_atlas_stream-6ml1n5
- hydrologic_zone_boundaries
- freshwater_atlas_stream_directions

stream_restrictions-5qgetu
- water_allocation_restrictions

pk_freshwater_atlas_watershed-cem099
- freshwater_atlas_watersheds
*/

export const devSources = {
  'mapbox://mapbox.satellite': {
    'url': 'mapbox://mapbox.satellite',
    'type': 'raster',
    'tileSize': 256
  },
  'composite': {
    'url': 'mapbox://mapbox.mapbox-streets-v8,' +
           'mapbox.mapbox-terrain-v2,' +
           'iit-water.bf1gc2mz,' + // hydat-879a50
           'iit-water.8rt7ts1c', // glaciers_and_isolines-28fnv1
    'type': 'vector'
  }
}

/*
Historical sources used in the production style on MapBox studio:
iit-water.448thhpa - 448thhpa
iit-water.6q8q0qac - 6q8q0qac
iit-water.first-nations - first-nations
iit-water.2svbut5f - 2svbut5f
iit-water.2ah76e1a - stream_restrictions-5qgetu
iit-water.36r1x37x - wally_vector_cadastral-dzg0md
iit-water.0tsq064k - 0tsq064k
iit-water.7iwr3fo1 - pk_freshwater_atlas_watershed-cem099

0tsq064k
- normal_annual_runoff_isolines
- bc_major_watersheds
- aquifers
- hydrologic_zone_boundaries

stream_restrictions-5qgetu
- water_allocation_restrictions

6q8q0qac
- freshwater_atlas_stream_networks

448thhpa
- water_licensed_works
- water_licensed_works_dash1
- water_licensed_works_dash2
- water_licensed_works_dash3
- water_licensed_works_dash4
- fish_obstacles
- fish_obstacles_old
- water_approval_points
- fish_observations
- fish_observations_summaries
- fish_observations_old

first-nations
- fn_treaty_lands
- fn_treaty_areas
- fn_community_locations

2svbut5f
- water_rights_applications

pk-hydat-6l5sgh
- hydrometric_stream_flow

pk_freshwater_atlas_watershed
- freshwater_atlas_watersheds

wally_vector_cadastral-dzg0md
- cadastral

wally_freshwater_atlas_stream-6ml1n5
- freshwater_atlas_stream_directions
 */
export const prodSources = {
  'mapbox://mapbox.satellite': {
    'url': 'mapbox://mapbox.satellite',
    'type': 'raster',
    'tileSize': 256
  },
  'composite': {
    'url': 'mapbox://mapbox.mapbox-streets-v8,' +
      'mapbox.mapbox-terrain-v2,' +
      'iit-water.31epl7h1,' + // pk-hydat-6l5sgh
      'iit-water.0tsq064k', // 0tsq064k
    'type': 'vector'
  }
}
