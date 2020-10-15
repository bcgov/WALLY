import * as metadata from './metadataUtils'
import layersWally from '../mapbox/layersWally'

export const API_URL = process.env.VUE_APP_AXIOS_BASE_URL

export function getMapLayerItemTitle (property) {
  return metadata.LAYER_PROPERTY_NAMES[metadata.LAYER_PROPERTY_MAPPINGS[property]]
}

export function getMapLayerItemValue (property) {
  return metadata.LAYER_PROPERTY_MAPPINGS[property]
}

// export function getMapLayerName (layerId) {
//   console.log(layerId)
//   let layer = metadata.DATA_MARTS.find(e => e.wmsLayer === layerId)
//   if (layer) { return layer.name }
// }

// export function getMapSubheading (id) {
//   let name = getMapLayerName(trimId(id))
//   if (name) {
//     name = name.slice(0, -1)
//     return name
//   }
// }

// export function trimId (id) {
//   return typeof (id) === 'string' ? id.substr(0, id.lastIndexOf('.')) : ''
// }

// Helper function to set a layer style for a source
export const addMapboxLayer = (map, id, sourceLayer) => {
  let layerStyles = layersWally[id]

  // Check if there are multiple layers for this source
  if (Array.isArray(layerStyles)) {
    layerStyles.forEach((layer) => {
      layer['source-layer'] = sourceLayer
      global.config.debug && console.log('[wally] adding wally layer for', id, layer, sourceLayer)
      map.addLayer(layer)
    })
  } else {
    layerStyles['source-layer'] = sourceLayer
    global.config.debug && console.log('[wally] adding wally layer for', id, layerStyles, sourceLayer)
    map.addLayer(layerStyles)
  }
}

// Helper function to create a vector source
export const addMapboxVectorSource = (map, id, url) => {
  let vectorSource = {
    'type': 'vector',
    'tiles': [url],
    'source-layer': id,
    'minzoom': 3,
    'maxzoom': 20
  }
  global.config.debug && console.log('[wally] add source', vectorSource)
  map.addSource(id, vectorSource)
}
