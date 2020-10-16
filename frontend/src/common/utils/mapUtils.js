import * as metadata from './metadataUtils'
import layersWally from '../mapbox/layersWally'

import { POINT, LINESTRING, POLYGON, pointFeature, lineStringFeature, polygonFeature } from '../mapbox/features'

export const API_URL = process.env.VUE_APP_AXIOS_BASE_URL

export function getMapLayerItemTitle (property) {
  return metadata.LAYER_PROPERTY_NAMES[metadata.LAYER_PROPERTY_MAPPINGS[property]]
}

export function getMapLayerItemValue (property) {
  return metadata.LAYER_PROPERTY_MAPPINGS[property]
}

export const findWallyLayer = (id) => {
  const layer = layersWally[id]
  if (Array.isArray(layer)) {
    console.error(`[wally] Cannot find a single layer ${id}`)
  }
  return layer
}

// Returns an array of wally layers
export const findWallyLayerArray = (id) => {
  // console.log('finding layer', id)
  // console.log(layersWally)
  const layers = layersWally[id]
  if (!Array.isArray(layers)) {
    return [layers]
  }
  return layers
}

// Helper function to set a layer style for a source
export const addMapboxLayer = (map, id, sourceLayer, before) => {
  let layers = findWallyLayerArray(id)

  layers.forEach((layer) => {
    // global.config.debug && console.log('[wally] padding wally layer for', id, layer, sourceLayer)
    if (sourceLayer !== undefined) {
      layer['source-layer'] = sourceLayer
    }
    if (before === undefined) {
      map.addLayer(layer)
    } else {
      map.addLayer(layer, before)
    }
  })
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
  // global.config.debug && console.log('[wally] add source', vectorSource)
  map.addSource(id, vectorSource)
}

export const createFeature = ({ id, geometryType, coordinates, properties = {} }) => {
  switch (geometryType) {
    case POINT:
      return pointFeature(id, coordinates, properties)
    case LINESTRING:
      return lineStringFeature(id, coordinates, properties)
    case POLYGON:
      return polygonFeature(id, coordinates, properties)
    default:
      return {}
  }
}
