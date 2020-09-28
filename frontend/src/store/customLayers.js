// Mapbox style config code borrowed from
// https://github.com/CrunchyData/pg_tileserv

import mapboxgl from 'mapbox-gl'

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

function popupText (properties) {
  const props = Object.entries(properties).map(prop => `${prop[0]}: ${prop[1]}`)
  return props.join('\n')
}

function geojsonSource ({ id, featureCollection }) {
  console.log(featureCollection)
  return {
    type: 'geojson',
    data: featureCollection
  }
}

export default {
  namespaced: true,
  state: {
    customLayers: {
      id: 'imported-map-layers',
      name: 'Imported Layers',
      children: []
    },
    selectedCustomLayers: []
  },
  mutations: {
    addCustomGeoJSONLayer (state, { map, featureCollection, geomType, color }) {
      // featureCollection should have an ID field and a name in properties.name

      const template = {
        id: featureCollection.id,
        name: featureCollection.properties.name,
        geomType: geomType,
        color: color
      }

      state.customLayers.children.push(template)
      map.addSource(featureCollection.id, geojsonSource({ id: featureCollection.id, featureCollection }))
      map.addLayer(layerConfig({ id: featureCollection.id, geomType, color }))
      state.selectedCustomLayers.push(featureCollection.id)

      // create popup on click, and have cursor change on hover
      map.on('click', featureCollection.id, function (e) {
        new mapboxgl.Popup({ className: 'custom-layer-popup' })
          .setMaxWidth('300px')
          .setLngLat(e.lngLat)
          .setText(popupText(e.features[0].properties))
          .addTo(map)
      })
      map.on('mouseenter', featureCollection.id, function (e) {
        map.getCanvas().style.cursor = 'pointer'
      })
      map.on('mouseleave', featureCollection.id, function (e) {
        map.getCanvas().style.cursor = ''
      })
    },
    removeCustomLayer (state, { map, id }) {
      // removes a custom layer by layer ID

      map.removeLayer(id)
      map.removeSource(id)

      const layerPos = state.customLayers.children.map(x => x.id).indexOf(id)
      if (layerPos > -1) {
        state.customLayers.children.splice(layerPos, 1)
      }
    },
    deselectCustomLayer (state, id) {
      const layerPos = state.selectedCustomLayers.indexOf(id)
      if (layerPos > -1) {
        state.selectedCustomLayers.splice(layerPos, 1)
      }
    }
  },
  actions: {
    loadCustomGeoJSONLayer ({ commit, dispatch }, { map, featureCollection, geomType, color }) {
      commit('addCustomGeoJSONLayer', { map, featureCollection, geomType, color })
    },
    unloadCustomLayer ({ commit, dispatch }, id) {
      commit('deselectCustomLayer', id)
      commit('removeCustomLayer', id)
    },
    setActiveCustomLayers ({ state, commit }, payload) {
      let prev = state.selectedCustomLayers
      prev.filter((l) => !payload.includes(l)).forEach((l) => commit('map/deactivateLayer', l, { root: true }))
      payload.filter((l) => !prev.includes(l)).forEach((l) => commit('map/activateLayer', l, { root: true }))
      state.selectedCustomLayers = payload
    }
  },
  getters: {
    customLayers: state => state.customLayers,
    selectedCustomLayers: state => state.selectedCustomLayers
  }
}
