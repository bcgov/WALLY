export const POINT = 'Point'
export const LINESTRING = 'LineString'
export const POLYGON = 'Polygon'
export const FEATURECOLLECTION = 'FeatureCollection'

export const pointFeature = (coordinates, properties = {}) => {
  return {
    type: 'Feature',
    geometry: {
      type: 'Point',
      coordinates
    },
    properties
  }
}

export const lineStringFeature = (coordinates, properties = {}) => {
  return {
    type: 'Feature',
    geometry: {
      type: 'LineString',
      coordinates
    },
    properties
  }
}

export const polygonFeature = (coordinates, properties = {}) => {
  return {
    type: 'Feature',
    geometry: {
      type: 'Polygon',
      coordinates
    },
    properties
  }
}

export const featureCollection = (features) => {
  return {
    type: 'FeatureCollection',
    features
  }
}

export const geojsonFC = (data) => {
  return {
    type: 'geojson',
    data
  }
}

export const vectorSource = (url, id, minZoom = 3, maxZoom = 20) => ({
  type: 'vector',
  tiles: [url],
  'source-layer': id,
  minzoom: minZoom,
  maxzoom: maxZoom
})
