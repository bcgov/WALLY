import L from 'leaflet'

export const wmsBaseURL = 'https://openmaps.gov.bc.ca/geo/pub/'

export function wmsParamString (payload) {
  let params = {
    request: 'GetMap',
    service: 'WMS',
    srs: 'EPSG:4326',
    version: '1.1.1',
    format: 'application/json;type=topojson',
    bbox: payload.bounds,
    height: payload.size.y,
    width: payload.size.x,
    layers: payload.layer
  }
  return L.Util.getParamString(params)
}

export function setLayerSource (map, layerId, source, sourceLayer) {
  const oldLayers = map.getStyle().layers;
  const layerIndex = oldLayers.findIndex(l => l.id === layerId);
  const layerDef = oldLayers[layerIndex];
  const before = oldLayers[layerIndex + 1] && oldLayers[layerIndex + 1].id;
  layerDef.source = source;
  if (sourceLayer) {
      layerDef['source-layer'] = sourceLayer;
  }
  map.removeLayer(layerId);
  map.addLayer(layerDef, before);
}