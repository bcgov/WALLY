// Mapbox style config code borrowed from
// https://github.com/CrunchyData/pg_tileserv

import mapboxgl from 'mapbox-gl'
import { geojsonFC } from '../common/mapbox/features'

function layerConfig ({ id, geomType, color }) {
  const paints = {
    'circle': {
      'circle-color': color,
      'circle-radius': 3,
      'circle-stroke-width': 1,
      'circle-stroke-color': '#333333'
    },
    'line': {
      'line-color': color,
      'line-width': 1.5
    },
    'fill': {
      'fill-color': color,
      'fill-outline-color': '#333333',
      'fill-opacity': 0.33
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
  console.log(paints[paint])
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

export default {
  namespaced: true,
  state: {
    customLayers: {
      id: '_imported-map-layers',
      type: 'category',
      name: 'Imported Layers',
      children: []
    },
    selectedCustomLayers: []
  },
  mutations: {
    registerCustomLayer (state, { layerInfo }) {
      // featureCollection should have an ID field and a name in properties.name
      state.customLayers.children.push(layerInfo)
      state.selectedCustomLayers.push(layerInfo.id)
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
      const layerInfo = {
        id: featureCollection.id,
        name: featureCollection.properties.name,
        geomType: geomType,
        color: color
      }

      // add the layer to the map within a promise. That way the component dispatching this action
      // can have some visibility into errors that might have occured while loading the layer.
      return new Promise((resolve, reject) => {
        try {
          map.addSource(featureCollection.id, geojsonFC(featureCollection))
          map.addLayer(layerConfig({ id: featureCollection.id, geomType, color }))

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

          commit('registerCustomLayer', { layerInfo })
          resolve()
        } catch (error) {
          reject(error)
        }
      })
    },
    unloadCustomLayer ({ commit, dispatch }, { map, id }) {
      commit('deselectCustomLayer', id)
      commit('removeCustomLayer', { map, id })
    },
    setActiveCustomLayers ({ state, commit }, payload) {
      let prev = state.selectedCustomLayers
      prev
        .filter((l) => l !== '_imported-map-layers')
        .filter((l) => !payload.includes(l)).forEach((l) => commit('map/deactivateLayer', l, { root: true }))
      payload
        .filter((l) => l !== '_imported-map-layers')
        .filter((l) => !prev.includes(l)).forEach((l) => commit('map/activateLayer', l, { root: true }))
      state.selectedCustomLayers = payload
    }
  },
  getters: {
    customLayers: state => state.customLayers,
    selectedCustomLayers: state => state.selectedCustomLayers
  }
}
