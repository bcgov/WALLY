import MapLegend from './MapLegend.vue'
import EventBus from '../../services/EventBus.js'
import { mapGetters, mapActions } from 'vuex'
import * as _ from 'lodash'
import { wmsBaseURL } from '../../utils/wmsUtils'
import mapboxgl from 'mapbox-gl'
import MapboxDraw from '@mapbox/mapbox-gl-draw'
import MapboxGeocoder from '@mapbox/mapbox-gl-geocoder'
import HighlightPoint from './MapHighlightPoint'
import * as metadata from '../../utils/metadataUtils'
import bbox from '@turf/bbox'

import qs from 'querystring'
import ApiService from '../../services/ApiService'

const point = {
  'type': 'Feature',
  'geometry': {
    'type': 'Point',
    'coordinates': [[]]
  }
}
const polygon = {
  'type': 'Feature',
  'geometry': {
    'type': 'Polygon',
    'coordinates': [[]]
  }
}

export default {
  name: 'Map',
  components: { MapLegend },
  mounted () {
    this.initMap()
    EventBus.$on('layer:added', this.handleAddWMSLayer)
    EventBus.$on('layer:removed', this.handleRemoveWMSLayer)
    EventBus.$on('dataMart:added', this.handleAddApiLayer)
    EventBus.$on('dataMart:removed', this.handleRemoveApiLayer)
    EventBus.$on('feature:added', this.handleAddFeature)
    EventBus.$on('layers:loaded', this.loadLayers)
    EventBus.$on('draw:reset', this.replaceOldFeatures)
    EventBus.$on('draw:redraw', () => this.handleSelect(this.draw.getAll()))
    EventBus.$on('highlight:clear', this.clearHighlightLayer)

    // this.$store.dispatch(FETCH_DATA_LAYERS)
  },
  beforeDestroy () {
    EventBus.$off('layer:added', this.handleAddWMSLayer)
    EventBus.$off('layer:removed', this.handleRemoveWMSLayer)
    EventBus.$off('dataMart:added', this.handleAddApiLayer)
    EventBus.$off('dataMart:removed', this.handleRemoveApiLayer)
    EventBus.$off('feature:added', this.handleAddFeature)
    EventBus.$off('layers:loaded', this.loadLayers)
    EventBus.$off('draw:reset', this.replaceOldFeatures)
    EventBus.$off('draw:redraw', () => this.handleSelect(this.draw.getAll()))
    EventBus.$off('highlight:clear', this.clearHighlightLayer)
  },
  data () {
    return {
      map: null,
      // legendControlContent: null,
      // activeLayerGroup: L.layerGroup(),
      // markerLayerGroup: L.layerGroup(),
      activeLayers: {},
      draw: null, // mapbox draw object (controls drawn polygons e.g. for area select)
      isDrawingToolActive: false
    }
  },
  computed: {
    ...mapGetters([
      'allMapLayers',
      'activeMapLayers',
      'allDataMarts',
      'activeDataMarts',
      'highlightFeatureData',
      'dataMartFeatureInfo'
    ])
  },
  methods: {
    async initMap () {
      // temporary public token with limited scope (reading layers) just for testing.

      const mapConfig = await ApiService.get('api/v1/map-config')
      mapboxgl.accessToken = mapConfig.data.mapbox_token

      this.map = new mapboxgl.Map({
        container: 'map', // container id
        style: 'mapbox://styles/iit-water/ck0pm9gqz6qiw1cnxrf9s8yu2', // stylesheet location
        center: [-124, 54.5], // starting position
        zoom: 4.7 // starting zoom
      })

      const clearSelections = () => {
        this.replaceOldFeatures()
        this.$store.commit('clearDataMartFeatures')
        this.$store.commit('clearDisplayTemplates')
      }

      const modes = MapboxDraw.modes
      modes.simple_select.onTrash = clearSelections
      modes.draw_polygon.onTrash = clearSelections
      modes.draw_point.onTrash = clearSelections

      this.draw = new MapboxDraw({
        modes: modes,
        displayControlsDefault: false,
        controls: {
          polygon: true,
          trash: true
        }
      })

      const geocoder = new MapboxGeocoder({
        accessToken: mapboxgl.accessToken,
        mapboxgl: this.map,
        origin: ApiService.baseURL,
        container: 'geocoder-container'
      })

      // Add zoom and rotation controls to the map.
      document.getElementById('geocoder').appendChild(geocoder.onAdd(this.map))
      this.map.addControl(new mapboxgl.NavigationControl(), 'top-left')
      this.map.addControl(this.draw, 'top-left')
      this.map.addControl(new mapboxgl.GeolocateControl({
        positionOptions: {
          enableHighAccuracy: true
        },
        showUserLocation: false
      }), 'top-left')
      this.map.on('style.load', () => {
        this.getMapLayers()
      })

      this.initHighlightLayers()
      this.listenForAreaSelect()

      // special handling for parcels because we may not want to have
      // users turn this layer on/off (it should always be on)
      this.map.on('click', 'parcels', this.setSingleFeature)
      this.map.on('mouseenter', 'parcels', this.setCursorPointer)
      this.map.on('mouseleave', 'parcels', this.resetCursor)

      // Subscribe to mode change event to toggle drawing state
      this.map.on('draw.modechange', this.handleModeChange)
    },
    handleModeChange (e) {
      if (e.mode == 'draw_polygon') {
        this.isDrawingToolActive = true
      } else if (e.mode == 'simple_select') {
        setTimeout(() => {
          this.isDrawingToolActive = false
        }, 500)
      }
    },
    initHighlightLayers () {
      this.map.on('load', () => {
        // initialize highlight layer
        this.map.addSource('highlightLayerData', { type: 'geojson', data: polygon })
        this.map.addLayer({
          'id': 'highlightLayer',
          'type': 'fill',
          'source': 'highlightLayerData',
          'layout': {},
          'paint': {
            'fill-color': 'rgba(154, 63, 202, 0.25)'
          }
        })
        this.map.addImage('highlight-point', HighlightPoint(this.map, 90), { pixelRatio: 2 })
        this.map.addSource('highlightPointData', { type: 'geojson', data: point })
        this.map.addLayer({
          'id': 'highlightPoint',
          'type': 'symbol',
          'source': 'highlightPointData',
          'layout': {
            'icon-image': 'highlight-point'
          }
        })
      })
    },
    loadLayers () {
      const layers = this.allMapLayers

      // load each layer, but default to no visibility.
      // the user can toggle layers on and off with the layer controls.
      for (let i = 0; i < layers.length; i++) {
        const layer = layers[i]

        // All layers are now vector based sourced from mapbox
        // so we don't need to check for layer type anymore
        const vector = layer['display_data_name']
        this.map.on('click', vector, this.setSingleFeature)
        this.map.on('mouseenter', vector, this.setCursorPointer)
        this.map.on('mouseleave', vector, this.resetCursor)
      }
    },
    updateHighlightLayerData (data) {
      if (data.geometry.type === 'Point') {
        this.map.getSource('highlightPointData').setData(data)
        this.map.getSource('highlightLayerData').setData(polygon)
      } else {
        this.map.getSource('highlightPointData').setData(point)
        this.map.getSource('highlightLayerData').setData(data)
      }
    },
    clearHighlightLayer () {
      this.map.getSource('highlightPointData').setData(point)
      this.map.getSource('highlightLayerData').setData(polygon)
    },
    handleAddFeature (f) {
      let p = L.latLng(f.lat, f.lng)
      if (p) {
        L.popup()
          .setLatLng(p)
          .setContent('Lat: ' + _.round(p.lat, 5) + ' Lng: ' + _.round(p.lng, 5))
          .openOn(this.map)
      }
    },
    handleAddWMSLayer (displayDataName) {
      this.map.setLayoutProperty(displayDataName, 'visibility', 'visible')
    },
    handleRemoveWMSLayer (displayDataName) {
      this.clearHighlightLayer()
      this.map.setLayoutProperty(displayDataName, 'visibility', 'none')
    },
    handleAddApiLayer (datamart) {
      const layer = this.activeDataMarts.find((x) => {
        return x.display_data_name === datamart.displayDataName
      })
      this.addGeoJSONLayer(layer)
    },
    handleRemoveApiLayer (displayDataName) {
      this.removeLayer(displayDataName)
    },
    addGeoJSONLayer (layer) {
      if (!layer || !layer.data) {
        console.error('invalid format for data source/data mart')
        return
      }

      // layer.data should have a "features" or "geojson" property, which
      // must be a list of geojson Features.  For example, layer.data could be
      // a FeatureCollection format object. The 'features' list will be added to the map.
      let features
      if (layer.data.features && layer.data.features.length) {
        features = layer.data.features
      } else if (layer.data.geojson && layer.data.geojson.length) {
        features = layer.data.geojson
      }
      if (!features) {
        console.error('could not find a features list or object to add to map')
        return
      }

      // this.activeLayers[layer.display_data_name] = L.geoJSON(features, {
      //   onEachFeature: function (feature, layer) {
      //     layer.bindPopup('<h3>' + feature.properties.name + '</h3><p>' + feature.properties.description + '</p>')
      //   }
      // })
      this.activeLayers[layer.display_data_name].addTo(this.map)
    },
    addWMSLayer (layer) {
      const layerID = layer.display_data_name || layer.wms_name || layer.display_name
      if (!layerID) {
        return
      }

      const wmsOpts = {
        service: 'WMS',
        request: 'GetMap',
        format: 'image/png',
        layers: 'pub:' + layer.wms_name,
        styles: layer.wms_style,
        transparent: true,
        name: layer.name,
        height: 256,
        width: 256,
        overlay: true,
        srs: 'EPSG:3857'
      }

      const query = qs.stringify(wmsOpts)
      const url = wmsBaseURL + layer.wms_name + '/ows?' + query + '&BBOX={bbox-epsg-3857}'

      const newLayer = {
        'id': layerID,
        'type': 'raster',
        'layout': {
          'visibility': 'none'
        },
        'source': {
          'type': 'raster',
          'tiles': [
            url
          ],
          'tileSize': 256
        }
      }

      this.map.addLayer(newLayer, 'groundwater_wells')
    },
    removeLayer (layer) {
      const displayDataName = layer.display_data_name || layer
      if (!displayDataName || !this.activeLayers[displayDataName]) {
        return
      }
      this.map.removeLayer(layer.id)
      // delete this.legendGraphics[layer.id]
      delete this.activeLayers[layer.id]
    },
    replaceOldFeatures (newFeature = null) {
      // replace all previously drawn features with the new one.
      // this has the effect of only allowing one selection box to be drawn at a time.
      const old = this.draw.getAll().features.filter((f) => f.id !== newFeature)
      this.draw.delete(old.map((feature) => feature.id))
    },
    handleSelect (feature) {
      if (!feature || !feature.features || !feature.features.length) return

      const newFeature = feature.features[0].id
      this.replaceOldFeatures(newFeature)

      // for drawn rectangular regions, the polygon describing the rectangle is the first
      // element in the array of drawn features.
      // note: this is what might break if extending the selection tools to draw more objects.
      const bounds = bbox(feature.features[0])
      this.getMapObjects(bounds)
      this.$store.commit('setSelectionBoundingBox', bounds)
      this.$store.commit('setLayerSelectionActiveState', false)
    },
    listenForAreaSelect () {
      this.map.on('draw.create', this.handleSelect)
      this.map.on('draw.update', this.handleSelect)
    },
    getMapObjects (bounds) {
      // TODO: Separate activeMaplayers by activeWMSLayers and activeDataMartLayers
      const canvas = this.map.getCanvas()
      const size = { x: canvas.width, y: canvas.height }

      this.$store.commit('clearDataMartFeatures')
      this.$store.dispatch('getDataMartFeatures', { bounds: bounds, size: size, layers: this.activeMapLayers })
    },
    setSingleFeature (e) {
      if (!this.isDrawingToolActive) {
        // Calls API and gets and sets feature data
        const feature = e.features[0]
        let payload = {
          display_data_name: feature.layer.id,
          pk: feature.properties[metadata.PRIMARY_KEYS[feature.layer.id]]
        }
        this.$store.dispatch('getDataMartFeatureInfo', payload)
      }
    },
    getPolygonCenter (arr) {
      if (arr.length === 1) { return arr }
      var x = arr.map(x => x[0])
      var y = arr.map(x => x[1])
      var cx = (Math.min(...x) + Math.max(...x)) / 2
      var cy = (Math.min(...y) + Math.max(...y)) / 2
      return [cx, cy]
    },
    getArrayDepth (value) {
      return Array.isArray(value) ? 1 + Math.max(...value.map(this.getArrayDepth)) : 0
    },
    formatLatLon (lon, lat) {
      // Formats lat lon to be within proper ranges
      lon = lon < 0 ? lon : -lon
      lat = lat > 0 ? lat : -lat
      return [lon, lat]
    },
    setCursorPointer () {
      this.map.getCanvas().style.cursor = 'pointer'
    },
    resetCursor () {
      this.map.getCanvas().style.cursor = ''
    },
    ...mapActions(['getMapLayers'])
  },
  watch: {
    highlightFeatureData (value) {
      if (value && value.geometry) {
        if (value.geometry.type == 'Point') {
          let coordinates = value.geometry.coordinates
          value.geometry.coordinates = this.formatLatLon(coordinates[0], coordinates[1])
        }
        this.updateHighlightLayerData(value)
      }
    },
    dataMartFeatureInfo (value) {
      if (value && value.geometry) {
        let coordinates = value.geometry.coordinates
        if (value.geometry.type == 'Point') {
          coordinates = this.formatLatLon(coordinates[0], coordinates[1])
          value.geometry.coordinates = coordinates
        } else {
          let depth = this.getArrayDepth(coordinates)
          let flattened = coordinates.flat(depth - 2)
          coordinates = this.getPolygonCenter(flattened)
        }
        this.map.flyTo({
          center: [coordinates[0], coordinates[1]]
        })
        this.updateHighlightLayerData(value)
      }
    }
  }
}
