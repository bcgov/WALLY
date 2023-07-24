import * as metadata from './metadataUtils'
import layersWally from '../mapbox/layersWally'

export const API_URL = process.env.VUE_APP_AXIOS_BASE_URL

export function getMapLayerItemTitle (property) {
  return metadata.LAYER_PROPERTY_NAMES[metadata.LAYER_PROPERTY_MAPPINGS[property]]
}

export function getMapLayerItemValue (property) {
  return metadata.LAYER_PROPERTY_MAPPINGS[property]
}

// Used to find a single layer, or a layer factory
export const findWallyLayer = (id) => {
  const layer = layersWally[id]
  if (Array.isArray(layer)) {
    console.error(`[wally] Cannot find a single layer ${id}`)
    return
  }
  return layer
}

// Returns an array of wally layers
export let findWallyLayerArray = (id) => {
  const layers = layersWally[id]
  if (!Array.isArray(layers)) {
    return [layers]
  }
  return layers
}

// Helper function to set a layer style for a source
export const addMapboxLayer = (map, id, { sourceLayer, before }) => {
  let layers = findWallyLayerArray(id)

  layers.forEach((layer) => {
    if (sourceLayer) {
      layer['source-layer'] = sourceLayer
    }
    if (before) {
      map.addLayer(layer, before)
    } else {
      map.addLayer(layer)
    }
  })
}
