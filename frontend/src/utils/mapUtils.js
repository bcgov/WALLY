import * as metadata from './metadataUtils'

export const API_URL = process.env.VUE_APP_AXIOS_BASE_URL

export function getMapLayerItemTitle (property) {
  return metadata.LAYER_PROPERTY_NAMES[metadata.LAYER_PROPERTY_MAPPINGS[property]]
}

export function getMapLayerItemValue (property) {
  return metadata.LAYER_PROPERTY_MAPPINGS[property]
}

export function getMapLayerName (layerId) {
  console.log(layerId)
  let layer = metadata.DATA_MARTS.find(e => e.wmsLayer === layerId)
  if (layer) { return layer.name }
}

export function getMapSubheading (id) {
  let name = getMapLayerName(trimId(id))
  if (name) {
    name = name.slice(0, -1)
    return name
  }
}

export function trimId (id) {
  return typeof (id) === 'string' ? id.substr(0, id.lastIndexOf('.')) : ''
}
