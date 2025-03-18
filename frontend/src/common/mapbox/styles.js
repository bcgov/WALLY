import { devSources, prodSources } from './sources'
import { devLayers, prodLayers } from './layersDefault'

const style = {
  version: 8,
  name: 'Wally Mapbox Style',
  metadata: {
    'mapbox:type': 'default',
    'mapbox:origin': 'outdoors-v11',
    'mapbox:autocomposite': true,
    'mapbox:groups': {
      1444855769305.6016: { name: 'Tunnels', collapsed: true },
      1444855786460.0557: { name: 'Roads', collapsed: true },
      1444855799204.86: { name: 'Bridges', collapsed: true },
      1444934295202.7542: {
        name: 'Admin boundaries',
        collapsed: true
      }
    },
    'mapbox:uiParadigm': 'layers'
  },
  center: [-122.9532242668688, 50.10213718910617],
  zoom: 12.840334576156339,
  bearing: 0,
  pitch: 0,
  sources: {},
  sprite: 'mapbox://sprites/iit-water/ck1s98x7p02q01cmso5jcx4cm/3oqjdz27e5jbpsfzu6ocic68q',
  glyphs: 'mapbox://fonts/iit-water/{fontstack}/{range}.pbf',
  layers: {},
  created: '2019-10-15T19:44:10.635Z',
  modified: '2020-09-10T17:21:00.744Z',
  id: 'ck1s98x7p02q01cmso5jcx4cm',
  owner: 'iit-water',
  visibility: 'private',
  draft: false
}

export const getDefaultStyle = () => {
  if (global.config.isDevelopment) {
    style.sources = devSources
    style.layers = devLayers
  }
  if (global.config.isStaging || global.config.isProduction) {
    style.sources = prodSources
    style.layers = prodLayers
  }
  return style
}
