// Mapbox style config code borrowed from
// https://github.com/CrunchyData/pg_tileserv

function layerConfig ({ id, geomType, color }) {
  const paints = {
    'circle': {
      'circle-color': color,
      'circle-radius': 3
    },
    'line': {
      'line-color': color,
      'line-width': 1.5
    },
    'fill': {
      'fill-color': color,
      'fill-outline-color': color,
      'fill-opacity': 0.1
    }
  }

  const painttypes = {
    'Point': 'circle',
    'MultiPoint': 'circle',
    'LineString': 'line',
    'MultiLineString': 'line',
    'Polygon': 'fill',
    'MultiPolygon': 'fill'
  }

  const paint = painttypes[geomType]

  return {
    'id': id,
    'source': id,
    'type': paint,
    'paint': paints[paint],
    'filter': ['match', ['geometry-type'], [geomType, 'Multi' + geomType], true, false]
  }
}

function geojsonSource ({ id, featureCollection }) {
  console.log(featureCollection)
  return {
    type: 'geojson',
    data: featureCollection
  }
}

export default {
  state: {
    customLayers: [],
    activeCustomLayers: []
  },
  mutations: {
    addCustomGeoJSONLayer (state, { map, featureCollection, geomType, color }) {
      // featureCollection should have an ID field and a name in properties.name
      state.customLayers.push(featureCollection)
      map.addSource(featureCollection.id, geojsonSource({ id: featureCollection.id, featureCollection }))
      map.addLayer(layerConfig({ id: featureCollection.id, geomType, color }))
      state.activeCustomLayers.push(featureCollection.id)
    },
    removeCustomLayer (state, { map, id }) {
      // removes a custom layer by layer ID

      map.removeLayer(id)
      map.removeSource(id)

      const layerPos = state.customLayers.map(x => x.id).indexOf(id)
      if (layerPos > -1) {
        state.customLayers.splice(layerPos, 1)
      }
    },
    activateCustomLayer (state, { map, id }) {
      state.activeCustomLayers.push(id)
    },
    deactiveCustomLayer (state, id) {
      const layerPos = state.activeCustomLayers.indexOf(id)
      if (layerPos > -1) {
        state.activeCustomLayers.splice(layerPos, 1)
      }
    }
  },
  actions: {
    loadCustomLayer ({ commit, dispatch }, { map, featureCollection, geomType, color }) {
      commit('addCustomGeoJSONLayer', { map, featureCollection, geomType, color })
    },
    unloadCustomLayer ({ commit, dispatch }, id) {
      commit('deactivateCustomLayer', id)
      commit('removeCustomLayer', id)
    }
  },
  getters: {
    customLayers: state => state.customLayers,
    activeCustomLayers: state => state.activeCustomLayers
  }
}
