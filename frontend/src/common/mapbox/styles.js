import sources from './sources'
import layers from './layers'

export default {
  'version': 8,
  'name': 'Wally Testing - Whistler Subset',
  'metadata': {
    'mapbox:type': 'default',
    'mapbox:origin': 'outdoors-v11',
    'mapbox:autocomposite': true,
    'mapbox:groups': {
      '1444855769305.6016': { 'name': 'Tunnels', 'collapsed': true },
      '1444855786460.0557': { 'name': 'Roads', 'collapsed': true },
      '1444855799204.86': { 'name': 'Bridges', 'collapsed': true },
      '1444934295202.7542': {
        'name': 'Admin boundaries',
        'collapsed': true
      }
    },
    'mapbox:sdk-support': {
      'js': '0.54.0',
      'android': '7.4.0',
      'ios': '4.11.0'
    },
    'mapbox:uiParadigm': 'layers'
  },
  'center': [-122.98521411124409, 50.06684480676634],
  'zoom': 10.953742704539236,
  'bearing': 0,
  'pitch': 0,
  sources,
  'sprite': 'mapbox://sprites/iit-water/ck22hx0391ch31dk9amwwr67x/dpqi93hdzhsmqqptk00gt4g0m',
  'glyphs': 'mapbox://fonts/iit-water/{fontstack}/{range}.pbf',
  layers,
  'created': '2019-10-22T23:44:32.806Z',
  'modified': '2020-09-08T14:31:04.326Z',
  'id': 'ck22hx0391ch31dk9amwwr67x',
  'owner': 'iit-water',
  'visibility': 'private',
  'draft': false
}
