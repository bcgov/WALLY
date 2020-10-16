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

// Returns an array of wally layers
export const findWallyLayers = (id) => {
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
  // let layerStyles = layersWally[id]
  // let layerToAdd = {}

  let layers = findWallyLayers(id)

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
  //
  // // Check if there are multiple layers for this source
  // if (Array.isArray(layerStyles)) {
  //   layerStyles.forEach((layer) => {
  //     layer['source-layer'] = sourceLayer
  //     global.config.debug && console.log('[wally] adding wally layer for', id, layer, sourceLayer)
  //     layerToAdd = layer
  //     // map.addLayer(layer)
  //   })
  // } else {
  //   layerStyles['source-layer'] = sourceLayer
  //   layerToAdd = layerStyles
  //   global.config.debug && console.log('[wally] adding wally layer for', id, layerStyles, sourceLayer)
  //   // map.addLayer(layerStyles)
  // }
  //
  // if (before === undefined) {
  //   map.addLayer(layerToAdd)
  // } else {
  //   map.addLayer(layerToAdd, before)
  // }
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
