/*
This file contains layer styling information about Wally-injected layers.
It is used as a reference lookup when adding a specific layer
 */
import {
  SOURCE_CUSTOM_SHAPE_DATA, SOURCE_DOWNSTREAM_NETWORK, SOURCE_FISH_OBSERVATIONS,
  SOURCE_HIGHLIGHT_LAYER_DATA,
  SOURCE_HIGHLIGHT_POINT_DATA,
  SOURCE_MEASUREMENT_LINE_HIGHLIGHT,
  SOURCE_MEASUREMENT_POLYGON_HIGHLIGHT,
  SOURCE_MEASUREMENT_SNAP_CIRCLE,
  SOURCE_SELECTED_STREAM,
  SOURCE_STREAM_APPORTIONMENT, SOURCE_UPSTREAM_NETWORK, SOURCE_WATER_APPROVALS,
  SOURCE_WATER_LICENCES, SOURCE_WATERSHEDS_AT_LOCATION, SOURCE_WS_HYDAT_STATIONS,
  SOURCE_WELL_OFFSET_DISTANCE
} from './sourcesWally'

export default {
  'aquifers': {
    'id': 'aquifers',
    'type': 'fill',
    'source': 'aquifers',
    'source-layer': 'aquifers',
    'layout': { 'visibility': 'none' },
    'paint': {
      'fill-color': 'hsla(190, 98%, 75%, 0.39)',
      'fill-outline-color': [
        'interpolate',
        ['linear'],
        ['zoom'],
        5,
        'hsla(0, 0%, 55%, 0)',
        10,
        'hsl(0, 0%, 19%)'
      ]
    }
  },
  'cadastral': {
    'id': 'cadastral',
    'type': 'fill',
    'source': 'cadastral',
    'source-layer': 'cadastral',
    'layout': { 'visibility': 'none' },
    'paint': {
      'fill-color': 'hsla(43, 98%, 55%, 0.4)',
      'fill-outline-color': 'hsl(0, 0%, 36%)'
    }
  },
  'freshwater_atlas_watersheds': {
    'id': 'freshwater_atlas_watersheds',
    'type': 'fill',
    'source': 'freshwater_atlas_watersheds',
    'source-layer': 'freshwater_atlas_watersheds',
    'layout': { 'visibility': 'none' },
    'paint': {
      'fill-color': 'hsla(271, 100%, 99%, 0.44)',
      'fill-outline-color': 'hsla(0, 0%, 33%, 0.58)'
    }
  },
  'freshwater_atlas_stream_directions': {
    'id': 'freshwater_atlas_stream_directions',
    'type': 'symbol',
    'source': 'freshwater_atlas_stream_directions',
    'source-layer': 'freshwater_atlas_stream_directions',
    'layout': {
      'icon-image': 'campsite-11',
      'icon-rotate':
        ['-', 90, ['to-number', ['get', 'DOWNSTREAM_DIRECTION']]],
      'icon-rotation-alignment': 'map',
      'visibility': 'none'
    },
    'paint': {}
  },
  'water_licensed_works': [
    {
      'id': 'water_licensed_works',
      'type': 'line',
      'source': 'water_licensed_works',
      'source-layer': 'water_licensed_works',
      'layout': { 'visibility': 'none' },
      'paint': {
        'line-color': [
          'match',
          ['get', 'FEATURE_CODE'],
          [
            'DB25150000',
            'DB00100000',
            'DA25100190',
            'DA25050180',
            'GB24300120'
          ],
          'hsl(0, 0%, 54%)',
          ['GB24300000'],
          'hsl(0, 100%, 59%)',
          ['GA08450000'],
          'hsl(0, 100%, 34%)',
          ['GE09400000'],
          'hsl(0, 0%, 100%)',
          ['GB09150000'],
          'hsl(117, 100%, 50%)',
          ['GA21050000', 'GB22100000', 'GA05200200', 'GB22100210'],
          'hsl(214, 100%, 53%)',
          ['PI11500000'],
          'hsl(40, 100%, 53%)',
          'hsla(0, 0%, 0%, 0)'
        ],
        'line-width': [
          'match',
          ['get', 'FEATURE_CODE'],
          ['GA08450000'],
          4,
          2
        ]
      }
    }, {
      'id': 'water_licensed_works_dash1',
      'type': 'line',
      'source': 'water_licensed_works',
      'source-layer': 'water_licensed_works',
      'layout': { 'visibility': 'none' },
      'paint': {
        'line-color': [
          'match',
          ['get', 'FEATURE_CODE'],
          ['EA06100200'],
          'hsl(0, 100%, 53%)',
          ['GA11500000'],
          'hsl(112, 100%, 44%)',
          ['EA21400610'],
          'hsl(0, 0%, 47%)',
          'hsla(0, 100%, 53%, 0)'
        ],
        'line-dasharray': [4, 1, 0.5, 1],
        'line-width': 2
      }
    }, {
      'id': 'water_licensed_works_dash2',
      'type': 'line',
      'source': 'water_licensed_works',
      'source-layer': 'water_licensed_works',
      'layout': { 'visibility': 'none' },
      'paint': {
        'line-color': [
          'match',
          ['get', 'FEATURE_CODE'],
          ['EA16400110'],
          'hsl(0, 0%, 50%)',
          'hsla(0, 0%, 44%, 0)'
        ],
        'line-dasharray': [3, 1, 0.5, 0.5, 0.5, 1],
        'line-width': 2
      }
    }, {
      'id': 'water_licensed_works_dash3',
      'type': 'line',
      'source': 'water_licensed_works',
      'source-layer': 'water_licensed_works',
      'layout': { 'visibility': 'none' },
      'paint': {
        'line-color': [
          'match',
          ['get', 'FEATURE_CODE'],
          ['GA08800000'],
          'hsl(0, 0%, 49%)',
          ['GA05200210'],
          'hsl(212, 100%, 47%)',
          'hsla(0, 0%, 0%, 0)'
        ],
        'line-dasharray': [2, 1],
        'line-width': 2
      }
    }, {
      'id': 'water_licensed_works_dash4',
      'type': 'line',
      'source': 'water_licensed_works',
      'source-layer': 'water_licensed_works',
      'layout': { 'visibility': 'none' },
      'paint': {
        'line-color': [
          'match',
          ['get', 'FEATURE_CODE'],
          ['GA28550000'],
          'hsl(0, 100%, 49%)',
          ['GA30350000'],
          'hsl(116, 100%, 50%)',
          'hsla(0, 0%, 0%, 0)'
        ],
        'line-dasharray': [4, 0.8, 1, 2],
        'line-width': 2
      }
    }],
  'freshwater_atlas_stream_networks': {
    'id': 'freshwater_atlas_stream_networks',
    'type': 'line',
    'source': 'freshwater_atlas_stream_networks',
    'source-layer': 'freshwater_atlas_stream_networks',
    'layout': { 'visibility': 'none' },
    'paint': { 'line-color': 'hsl(213, 78%, 55%)' }
  },
  'water_allocation_restrictions': {
    'id': 'water_allocation_restrictions',
    'type': 'line',
    'source': 'water_allocation_restrictions',
    'source-layer': 'water_allocation_restrictions',
    // 'source': 'composite',
    // 'source-layer': 'WLS_STREAM_RESTRICTIONS_SP',
    'layout': { 'visibility': 'none' },
    'paint': {
      'line-color': [
        'case',
        [
          'match',
          ['get', 'PRIMARY_RESTRICTION_CODE'],
          ['OR'],
          true,
          false
        ],
        'hsl(302, 88%, 61%)',
        [
          'match',
          ['get', 'PRIMARY_RESTRICTION_CODE'],
          ['FR'],
          true,
          false
        ],
        'hsl(0, 83%, 51%)',
        [
          'match',
          ['get', 'PRIMARY_RESTRICTION_CODE'],
          ['FR_EXC'],
          true,
          false
        ],
        'hsl(19, 64%, 35%)',
        [
          'match',
          ['get', 'PRIMARY_RESTRICTION_CODE'],
          ['PWS'],
          true,
          false
        ],
        'hsl(124, 93%, 31%)',
        [
          'match',
          ['get', 'PRIMARY_RESTRICTION_CODE'],
          ['PWS', 'RNW'],
          true,
          false
        ],
        'hsl(65, 98%, 31%)',
        'hsl(0, 0%, 64%)'
      ],
      'line-width': [
        'interpolate',
        ['linear'],
        ['zoom'],
        0,
        1,
        8,
        1,
        10,
        2,
        12,
        3,
        22,
        3
      ],
      'line-opacity': 0.67
    }
  },
  'bc_major_watersheds': {
    'id': 'bc_major_watersheds',
    'type': 'fill',
    'source': 'bc_major_watersheds',
    'source-layer': 'bc_major_watersheds',
    'layout': { 'visibility': 'none' },
    'paint': {
      'fill-color': [
        'interpolate',
        ['linear'],
        ['zoom'],
        0,
        'hsla(0, 100%, 100%, 0.5)',
        10,
        'hsla(0, 100%, 100%, 0.48)'
      ],
      'fill-outline-color': 'hsla(0, 0%, 18%, 0.59)'
    }
  },
  'freshwater_atlas_glaciers': {
    'id': 'freshwater_atlas_glaciers',
    'type': 'fill',
    'source': 'freshwater_atlas_glaciers',
    'source-layer': 'freshwater_atlas_glaciers',
    'layout': { 'visibility': 'none' },
    'paint': {
      'fill-color': 'hsla(210, 100%, 44%, 0.25)',
      'fill-outline-color': 'hsl(210, 100%, 50%)'
    }
  },
  'hydrologic_zone_boundaries': {
    'id': 'hydrologic_zone_boundaries',
    'type': 'fill',
    'source': 'hydrologic_zone_boundaries',
    'source-layer': 'hydrologic_zone_boundaries',
    'layout': { 'visibility': 'none' },
    'paint': {
      'fill-color': 'hsla(175, 100%, 78%, 0.2)',
      'fill-outline-color': 'hsl(208, 100%, 56%)'
    }
  },
  'critical_habitat_species_at_risk': {
    'id': 'critical_habitat_species_at_risk',
    'type': 'fill',
    'source': 'critical_habitat_species_at_risk',
    'source-layer': 'critical_habitat_species_at_risk',
    'layout': { 'visibility': 'none' },
    'paint': {
      'fill-color': [
        'interpolate',
        ['exponential', 1],
        ['zoom'],
        6,
        'hsla(45, 100%, 58%, 0.28)',
        10,
        'hsla(45, 100%, 58%, 0.62)',
        15,
        'hsla(45, 100%, 58%, 0.8)'
      ],
      'fill-outline-color': [
        'interpolate',
        ['linear'],
        ['zoom'],
        6,
        'hsla(0, 0%, 16%, 0)',
        13,
        'hsla(0, 0%, 16%, 0.7)'
      ]
    }
  },
  'ecocat_water_related_reports': {
    'id': 'ecocat_water_related_reports',
    'type': 'circle',
    'source': 'ecocat_water_related_reports',
    'source-layer': 'ecocat_water_related_reports',
    'layout': { 'visibility': 'none' },
    'paint': {
      'circle-color': 'hsl(192, 92%, 46%)',
      'circle-stroke-width': 1,
      'circle-stroke-color': 'hsl(207, 91%, 31%)',
      'circle-radius': [
        'interpolate',
        ['linear'],
        ['zoom'],
        0,
        1,
        22,
        5
      ],
      'circle-stroke-opacity': [
        'interpolate',
        ['linear'],
        ['zoom'],
        4,
        0,
        8,
        1
      ],
      'circle-opacity': [
        'interpolate',
        ['linear'],
        ['zoom'],
        0,
        0,
        8,
        1
      ]
    }
  },
  'bc_wildfire_active_weather_stations': {
    'id': 'bc_wildfire_active_weather_stations',
    'type': 'circle',
    'source': 'bc_wildfire_active_weather_stations',
    'source-layer': 'bc_wildfire_active_weather_stations',
    'layout': { 'visibility': 'none' },
    'paint': {
      'circle-color': 'hsl(40, 50%, 86%)',
      'circle-stroke-width': 1,
      'circle-stroke-color': 'hsl(120, 47%, 31%)',
      'circle-radius': [
        'interpolate',
        ['linear'],
        ['zoom'],
        0,
        1,
        15,
        5
      ],
      'circle-stroke-opacity': [
        'interpolate',
        ['linear'],
        ['zoom'],
        4,
        0.61,
        13,
        1
      ]
    }
  },
  'automated_snow_weather_station_locations': {
    'id': 'automated_snow_weather_station_locations',
    'type': 'circle',
    'source': 'automated_snow_weather_station_locations',
    'source-layer': 'automated_snow_weather_station_locations',
    'layout': { 'visibility': 'none' },
    'paint': {
      'circle-color': [
        'interpolate',
        ['exponential', 1],
        ['zoom'],
        2,
        'hsla(2, 100%, 100%, 0.4)',
        7,
        'hsl(2, 1%, 100%)'
      ],
      'circle-stroke-color': 'hsl(140, 95%, 52%)',
      'circle-stroke-width': 1,
      'circle-radius': [
        'interpolate',
        ['linear'],
        ['zoom'],
        0,
        1,
        15,
        5
      ]
    }
  },
  'water_rights_licences': {
    'id': 'water_rights_licences',
    'type': 'circle',
    'source': 'water_rights_licences',
    'source-layer': 'water_rights_licences',
    'layout': { 'visibility': 'none' },
    'paint': {
      'circle-color': [
        'match',
        ['get', 'POD_SUBTYPE'],
        ['POD'],
        'hsl(99, 71%, 57%)',
        ['PG', 'PWD'],
        'hsl(233, 77%, 66%)',
        '#6675eb'
      ],
      'circle-stroke-width': 1,
      'circle-stroke-color': [
        'match',
        ['get', 'POD_SUBTYPE'],
        ['POD'],
        'hsl(167, 64%, 27%)',
        'hsl(268, 64%, 27%)'
      ],
      'circle-stroke-opacity': [
        'interpolate',
        ['linear'],
        ['zoom'],
        5,
        0,
        15,
        1
      ],
      'circle-radius': [
        'interpolate',
        ['linear'],
        ['zoom'],
        0,
        1,
        15,
        5
      ],
      'circle-opacity': [
        'interpolate',
        ['linear'],
        ['zoom'],
        0,
        0,
        9,
        1
      ]
    }
  },
  'groundwater_wells': {
    'id': 'groundwater_wells',
    'type': 'circle',
    'source': 'groundwater_wells',
    'source-layer': 'groundwater_wells',
    'layout': { 'visibility': 'none' },
    'paint': {
      'circle-color': 'hsl(217, 99%, 50%)',
      'circle-stroke-color': [
        'interpolate',
        ['linear'],
        ['zoom'],
        5,
        'hsla(217, 100%, 57%, 0)',
        15,
        '#0141a7'
      ],
      'circle-stroke-width': 1,
      'circle-radius': [
        'interpolate',
        ['linear'],
        ['zoom'],
        0,
        1,
        15,
        5
      ],
      'circle-opacity': [
        'interpolate',
        ['linear'],
        ['zoom'],
        0,
        0,
        9,
        1
      ]
    }
  },
  'water_rights_applications': {
    'id': 'water_rights_applications',
    'type': 'circle',
    'source': 'water_rights_applications',
    'source-layer': 'water_rights_applications',
    'layout': { 'visibility': 'none' },
    'paint': {
      'circle-color': 'hsl(298, 95%, 32%)',
      'circle-stroke-color': 'hsl(290, 88%, 22%)',
      'circle-stroke-width': 1,
      'circle-stroke-opacity': [
        'interpolate',
        ['linear'],
        ['zoom'],
        5,
        0,
        10,
        1
      ],
      'circle-radius': [
        'interpolate',
        ['linear'],
        ['zoom'],
        0,
        1,
        16,
        5
      ],
      'circle-opacity': [
        'interpolate',
        ['linear'],
        ['zoom'],
        0,
        0,
        9,
        1
      ]
    }
  },
  'fn_community_locations': {
    'id': 'fn_community_locations',
    'type': 'circle',
    'source': 'fn_community_locations',
    'source-layer': 'fn_community_locations',
    'layout': { 'visibility': 'none' },
    'paint': {
      'circle-color': 'hsl(203, 80%, 35%)',
      'circle-stroke-color': 'hsl(200, 79%, 26%)',
      'circle-stroke-width': [
        'interpolate',
        ['linear'],
        ['zoom'],
        0,
        0,
        10,
        1
      ],
      'circle-radius': [
        'interpolate',
        ['linear'],
        ['zoom'],
        0,
        1,
        15,
        5
      ],
      'circle-opacity': [
        'interpolate',
        ['linear'],
        ['zoom'],
        0,
        0.5,
        10,
        1
      ]
    }
  },
  'fn_treaty_areas': {
    'id': 'fn_treaty_areas',
    'type': 'fill',
    'source': 'fn_treaty_areas',
    'source-layer': 'fn_treaty_areas',
    'layout': { 'visibility': 'none' },
    'paint': {
      'fill-color': 'hsla(147, 76%, 61%, 0.14)',
      'fill-outline-color': 'hsl(153, 67%, 18%)'
    }
  },
  'fn_treaty_lands': {
    'id': 'fn_treaty_lands',
    'type': 'fill',
    'source': 'fn_treaty_lands',
    'source-layer': 'fn_treaty_lands',
    'layout': { 'visibility': 'none' },
    'paint': {
      'fill-color': 'hsla(291, 80%, 23%, 0.19)',
      'fill-outline-color': 'hsl(250, 76%, 39%)'
    }
  },
  'fish_observations': {
    'id': 'fish_observations',
    'type': 'symbol',
    'source': 'fish_observations',
    'source-layer': 'fish_observations',
    'layout': { 'icon-image': 'fish-icon-orange', 'visibility': 'none' },
    'paint': {
      'icon-opacity': 0.8
    },
    'filter': ['==', 'POINT_TYPE_CODE', 'Observation']
  },
  'fish_observations_summaries': {
    'id': 'fish_observations_summaries',
    'type': 'symbol',
    'source': 'fish_observations',
    'source-layer': 'fish_observations',
    'layout': { 'icon-image': 'fish-icon-red', 'visibility': 'none' },
    'paint': {
      'icon-opacity': 0.8
    },
    'filter': ['==', 'POINT_TYPE_CODE', 'Summary']
  },
  'water_approval_points': {
    'id': 'water_approval_points',
    'type': 'circle',
    'source': 'water_approval_points',
    'source-layer': 'water_approval_points',
    'layout': { 'visibility': 'none' },
    'paint': {
      'circle-color': [
        'match',
        ['get', 'APPROVAL_STATUS'],
        ['Current'],
        'hsl(67, 100%, 55%)',
        ['Refuse/Abandoned', 'Cancelled'],
        'hsl(37, 98%, 49%)',
        'hsl(37, 100%, 53%)'
      ],
      'circle-stroke-width': 1,
      'circle-stroke-color': 'hsl(0, 0%, 31%)',
      'circle-radius': [
        'interpolate',
        ['linear'],
        ['zoom'],
        0,
        1,
        15,
        5
      ],
      'circle-opacity': [
        'interpolate',
        ['linear'],
        ['zoom'],
        0,
        0,
        9,
        1
      ],
      'circle-stroke-opacity': [
        'interpolate',
        ['linear'],
        ['zoom'],
        5,
        0,
        15,
        1
      ]
    }
  },
  'fish_obstacles': {
    'id': 'fish_obstacles',
    'type': 'symbol',
    'source': 'fish_obstacles',
    'source-layer': 'fish_obstacles',
    'layout': {
      'icon-image': 'x-btn',
      'icon-size': 0.75,
      'visibility': 'none'
    },
    'paint': { 'icon-opacity': 0.8 }
  },
  /*
  Other layers not shown in layer list but used heavily within wally
   */
  [SOURCE_WATER_LICENCES]: (data, max) => ({
    id: 'waterLicences',
    type: 'circle',
    source: {
      type: 'geojson',
      data: data
    },
    paint: {
      'circle-color': '#00796b',
      'circle-radius': [
        'interpolate',
        ['linear'],
        ['number', ['get', 'qty_m3_yr'], 0],
        0,
        10,
        max,
        max > 1000000 ? 50 : 25
      ],
      'circle-opacity': 0.5
    }
  }),
  [SOURCE_WS_HYDAT_STATIONS]: (data) => ({
    id: SOURCE_WS_HYDAT_STATIONS,
    type: 'circle',
    source: {
      type: 'geojson',
      data: data
    },
    paint: {
      'circle-color': '#ff33d4',
      'circle-radius': 7,
      'circle-opacity': 0.5
    }
  }),
  [SOURCE_CUSTOM_SHAPE_DATA]: {
    'id': 'customShape',
    'type': 'fill',
    'source': SOURCE_CUSTOM_SHAPE_DATA,
    'layout': {},
    'paint': {
      'fill-color': 'rgba(26, 193, 244, 0.08)',
      'fill-outline-color': 'rgb(8, 159, 205)'
    }
  },
  [SOURCE_HIGHLIGHT_LAYER_DATA]: {
    'id': 'highlightLayer',
    'type': 'fill',
    'source': SOURCE_HIGHLIGHT_LAYER_DATA,
    'layout': {},
    'paint': {
      'fill-color': 'rgba(154, 63, 202, 0.25)'
    }
  },
  [SOURCE_HIGHLIGHT_POINT_DATA]: {
    'id': 'highlightPoint',
    'type': 'symbol',
    'source': SOURCE_HIGHLIGHT_POINT_DATA,
    'layout': {
      'icon-image': 'highlight-point'
    }
  },
  [SOURCE_MEASUREMENT_POLYGON_HIGHLIGHT]: {
    'id': 'measurementPolygonHighlight',
    'type': 'fill',
    'source': SOURCE_MEASUREMENT_POLYGON_HIGHLIGHT,
    'layout': {},
    'paint': {
      'fill-color': 'rgba(26, 193, 244, 0.1)',
      'fill-outline-color': 'rgb(8, 159, 205)'
    }
  },
  [SOURCE_MEASUREMENT_SNAP_CIRCLE]: {
    'id': 'measurementSnapCircle',
    'type': 'fill',
    'source': SOURCE_MEASUREMENT_SNAP_CIRCLE,
    'layout': {},
    'paint': {
      'fill-color': 'rgba(255, 255, 255, 0.65)',
      'fill-outline-color': 'rgb(155, 155, 155)'
    }
  },
  [SOURCE_MEASUREMENT_LINE_HIGHLIGHT]: {
    'id': 'measurementLineHighlight',
    'type': 'line',
    'source': SOURCE_MEASUREMENT_LINE_HIGHLIGHT,
    'layout': {
      'line-join': 'round',
      'line-cap': 'round'
    },
    'paint': {
      'line-color': 'rgba(26, 193, 244, 0.7)',
      'line-width': 2
    }
  },
  [SOURCE_WATER_APPROVALS]: (max = 100000000) => ([
    {
      id: 'waterApprovals',
      type: 'circle',
      source: SOURCE_WATER_APPROVALS,
      paint: {
        'circle-color': '#FFE41A',
        'circle-radius': [
          'interpolate',
          ['linear'],
          ['number', ['get', 'qty_m³_yr'], 0],
          0,
          10,
          max,
          max > 1000000 ? 50 : 25
        ],
        'circle-opacity': 0.5
      }
    },
    {
      id: 'waterApprovalsCoverPoints',
      type: 'circle',
      source: SOURCE_WATER_APPROVALS,
      paint: {
        'circle-color': '#FFE41A',
        'circle-radius': 5,
        'circle-opacity': 1,
        'circle-stroke-width': 2,
        'circle-stroke-color': '#ffffff'
      }
    }
  ]),
  [SOURCE_WELL_OFFSET_DISTANCE]: {
    id: 'wellOffsetDistance',
    type: 'circle',
    source: SOURCE_WELL_OFFSET_DISTANCE,
    paint: {
      'circle-color': '#FFE41A',
      'circle-radius': 5,
      'circle-opacity': 0.5,
      'circle-stroke-width': 2,
      'circle-stroke-color': '#ffffff'
    }
  },
  [SOURCE_FISH_OBSERVATIONS]: (data) => ({
    id: 'fishObservations',
    type: 'circle',
    source: {
      type: 'geojson',
      data: data
    },
    paint: {
      'circle-color': '#B22222',
      'circle-radius': 5,
      'circle-opacity': 0
    }
  }),
  [SOURCE_WATERSHEDS_AT_LOCATION]: (watershedID, data) => ({
    id: watershedID,
    type: 'fill',
    source: {
      type: 'geojson',
      data: data
    },
    layout: {
      visibility: 'none'
    },
    paint: {
      'fill-color': '#039be5',
      'fill-outline-color': '#003366',
      'fill-opacity': 0.3
    }
  }),
  [SOURCE_UPSTREAM_NETWORK]: (data) => ({
    id: 'upstreamNetwork',
    type: 'fill',
    source: {
      type: 'geojson',
      data: data.upstream_poly
    },
    layout: {
      visibility: 'visible'
    },
    paint: {
      'fill-color': '#99CC99',
      'fill-outline-color': '#002171',
      'fill-opacity': 0.65
    }
  }),
  [SOURCE_DOWNSTREAM_NETWORK]: (data) => ({
    id: 'downstreamNetwork',
    type: 'fill',
    source: {
      type: 'geojson',
      data: data.downstream_poly
    },
    layout: {
      visibility: 'visible'
    },
    paint: {
      'fill-color': '#0d47a1',
      'fill-outline-color': '#002171',
      'fill-opacity': 0.5
    }
  }),
  // Stream sources
  // 'selectedStream': {
  //   'id': 'selectedStream',
  //   'type': 'line',
  //   'source': 'selectedStreamSource',
  //   'layout': {
  //     'line-join': 'round',
  //     'line-cap': 'round'
  //   },
  //   'paint': {
  //     'line-color': '#1500ff',
  //     'line-width': 3
  //   }
  // },
  'upstreamSource': {
    'id': 'upstream',
    'type': 'line',
    'source': 'upstreamSource',
    'layout': {
      'line-join': 'round',
      'line-cap': 'round'
    },
    'paint': {
      'line-color': '#00ff26',
      'line-width': 3
    }
  },
  'downstreamSource': {
    'id': 'downstream',
    'type': 'line',
    'source': 'downstreamSource',
    'layout': {
      'line-join': 'round',
      'line-cap': 'round'
    },
    'paint': {
      'line-color': '#ff4800',
      'line-width': 3
    }
  },
  'selectedStreamBufferSource': {
    'id': 'selectedStreamBuffer',
    'type': 'fill',
    'source': 'selectedStreamBufferSource',
    'layout': {
    },
    'paint': {
      'fill-color': 'rgba(21, 0, 255, 0.25)'
    }
  },
  'upstreamBufferSource': {
    'id': 'upstreamBuffer',
    'type': 'fill',
    'source': 'upstreamBufferSource',
    'layout': {
    },
    'paint': {
      'fill-color': 'rgba(0, 255, 38, 0.25)'
    }
  },
  'downstreamBufferSource': {
    'id': 'downstreamBuffer',
    'type': 'fill',
    'source': 'downstreamBufferSource',
    'layout': {
    },
    'paint': {
      'fill-color': 'rgba(255, 72, 0, 0.25)'
    }
  },
  [SOURCE_SELECTED_STREAM]: {
    'id': 'selectedStream',
    'type': 'line',
    'source': SOURCE_SELECTED_STREAM,
    'layout': {
      'line-join': 'round',
      'line-cap': 'round'
    },
    'paint': {
      'line-color': '#1500ff',
      'line-width': 3
    }
  },
  [SOURCE_STREAM_APPORTIONMENT]: [
    {
      'id': 'closestPointsOnStream',
      'type': 'circle',
      'source': SOURCE_STREAM_APPORTIONMENT,
      'layout': {},
      'paint': {
        'circle-color': 'rgb(255,83,212)',
        'circle-radius': 2,
        'circle-stroke-width': 1
      }
    },
    {
      'id': 'distanceLinesFromStream',
      'type': 'line',
      'source': SOURCE_STREAM_APPORTIONMENT,
      'layout': {},
      'paint': {
        'line-color': 'rgb(55,184,228)',
        'line-width': 3
      }
    },
    {
      'id': 'distanceLinesTextFromStream',
      'type': 'symbol',
      'source': SOURCE_STREAM_APPORTIONMENT,
      'layout': {
        'symbol-placement': 'line',
        'text-font': ['Open Sans Regular'],
        'text-field': '{title}',
        'text-size': 12
      }
    }
  ]
}
