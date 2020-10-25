export const POINT = 'Point'
export const LINESTRING = 'LineString'
export const POLYGON = 'Polygon'
export const FEATURECOLLECTION = 'FeatureCollection'

export const pointFeature = (coordinates, properties = {}) => {
  return {
    'type': 'Feature',
    'geometry': {
      'type': 'Point',
      'coordinates': coordinates
    },
    'properties': properties
  }
}

export const lineStringFeature = (coordinates, properties = {}) => {
  return {
    'type': 'Feature',
    'geometry': {
      'type': 'LineString',
      'coordinates': coordinates
    },
    'properties': properties
  }
}

export const polygonFeature = (coordinates, properties = {}) => {
  return {
    'type': 'Feature',
    'geometry': {
      'type': 'Polygon',
      'coordinates': coordinates
    },
    'properties': properties
  }
}

export const featureCollection = (features) => {
  return {
    type: 'FeatureCollection',
    features: features
  }
}

export const geojsonFC = (data) => {
  return {
    type: 'geojson',
    data: data
  }
}

export const vectorSource = (url, id, minZoom = 3, maxZoom = 20) => ({
  'type': 'vector',
  'tiles': [url],
  'source-layer': id,
  'minzoom': minZoom,
  'maxzoom': maxZoom
})
