import MapLegend from './MapLegend.vue'
import EventBus from '../../services/EventBus.js'
import { mapGetters, mapActions, mapMutations } from 'vuex'
import { wmsBaseURL } from '../../utils/wmsUtils'
import mapboxgl from 'mapbox-gl'
import MapboxDraw from '@mapbox/mapbox-gl-draw'
import MapboxGeocoder from '@mapbox/mapbox-gl-geocoder'
import MapScale from './MapScale'
import circle from '@turf/circle'
import coordinatesGeocoder from './localGeocoder'
import * as streamConfig from '../../utils/streamHighlights.config'

import { getArrayDepth } from '../../helpers'

import qs from 'querystring'
import ApiService from '../../services/ApiService'

// const point = {
//   'type': 'Feature',
//   'geometry': {
//     'type': 'Point',
//     'coordinates': [[]]
//   }
// }
// const polygon = {
//   'type': 'Feature',
//   'geometry': {
//     'type': 'Polygon',
//     'coordinates': [[]]
//   }
// }

export default {
  name: 'Map',
  components: { MapLegend },
  mounted () {
    this.initMap()
    // EventBus.$on('layer:added', this.handleAddLayer)
    // EventBus.$on('layer:removed', this.handleRemoveLayer)
    // EventBus.$on('baseLayer:added', this.handleAddBaseLayer)
    // EventBus.$on('baseLayer:removed', this.handleRemoveBaseLayer)
    // EventBus.$on('dataMart:added', this.handleAddApiLayer)
    // EventBus.$on('dataMart:removed', this.handleRemoveApiLayer)
    // EventBus.$on('layers:loaded', this.loadLayers)
    // EventBus.$on('draw:reset', this.replaceOldFeatures)
    // EventBus.$on('shapes:add', this.addShape)
    // EventBus.$on('shapes:reset', this.removeShapes)
    // EventBus.$on('draw:redraw', (opts) => this.handleSelect(this.draw.getAll(), opts))
    // EventBus.$on('highlight:clear', this.clearHighlightLayer)

    // this.$store.dispatch(FETCH_DATA_LAYERS)
  },
  beforeDestroy () {
    // EventBus.$off('layer:added', this.handleAddLayer)
    // EventBus.$off('layer:removed', this.handleRemoveLayer)
    // EventBus.$off('baseLayer:added', this.handleAddBaseLayer)
    // EventBus.$off('baseLayer:removed', this.handleRemoveBaseLayer)
    // EventBus.$off('dataMart:added', this.handleAddApiLayer)
    // EventBus.$off('dataMart:removed', this.handleRemoveApiLayer)
    // EventBus.$off('layers:loaded', this.loadLayers)
    // EventBus.$off('draw:reset', this.replaceOldFeatures)
    // EventBus.$off('shapes:add', this.addShape)
    // EventBus.$off('shapes:reset', this.removeShapes)
    // EventBus.$off('draw:redraw', () => this.handleSelect(this.draw.getAll()))
    // EventBus.$off('highlight:clear', this.clearHighlightLayer)
  },
  data () {
    return {
      // legendControlContent: null,
      // activeLayerGroup: L.layerGroup(),
      // markerLayerGroup: L.layerGroup(),
      lastZoom: 6,
      activeLayers: {},
      isDrawingToolActive: false
    }
  },
  computed: {
    mapStyle () {
      // todo: move the panel width to the store & grab that value instead
      //  of just 300px
      // if (this.infoPanelVisible) {
      //   return {
      //     left: '300px',
      //     width: 'calc(100vw - 300px)'
      //   }
      // }
      return {
        left: 0,
        width: '100%'
      }
    },
    ...mapGetters('map', [
      'allMapLayers',
      'activeMapLayers',
      'allDataMarts',
      'highlightFeatureData',
      'highlightFeatureCollectionData',
      'map',
      'draw',
      'geocoder'
    ]),
    ...mapGetters([
      'activeDataMarts',
      'dataMartFeatureInfo',
      'getSelectedStreamData',
      'getUpstreamData',
      'getDownstreamData',
      'getStreamSources',
      'getStreamLayers',
      'getSelectedStreamBufferData',
      'getUpstreamBufferData',
      'getDownstreamBufferData'
    ])
  },
  methods: {
    async initMap () {
      // temporary public token with limited scope (reading layers) just for testing.

      const mapConfig = await ApiService.get('api/v1/config/map')
      mapboxgl.accessToken = mapConfig.data.mapbox_token

      const zoomConfig = {
        center: process.env.VUE_APP_MAP_CENTER ? JSON.parse(process.env.VUE_APP_MAP_CENTER) : [-124, 54.5],
        zoomLevel: process.env.VUE_APP_MAP_ZOOM_LEVEL ? process.env.VUE_APP_MAP_ZOOM_LEVEL : 4.7
      }

      this.setMap(new mapboxgl.Map({
        container: 'map', // container id
        style: mapConfig.data.mapbox_style, // dev or prod map style
        center: zoomConfig.center, // starting position
        zoom: zoomConfig.zoomLevel, // starting zoom
        attributionControl: false, // hide default and re-add to the top left
        preserveDrawingBuffer: true // allows image export of the map at the cost of some performance
      }))

      const modes = MapboxDraw.modes
      modes.simple_select.onTrash = this.clearSelections
      modes.draw_polygon.onTrash = this.clearSelections
      modes.draw_point.onTrash = this.clearSelections
      modes.direct_select.onTrash = this.clearSelections

      this.setDraw(new MapboxDraw({
        modes: modes,
        displayControlsDefault: false,
        controls: {
          // polygon: true,
          // point: true,
          // line_string: true,
          trash: true
        }
      }))

      this.setGeocoder(new MapboxGeocoder({
        accessToken: mapboxgl.accessToken,
        mapboxgl: this.map,
        origin: ApiService.baseURL,
        marker: false,
        localGeocoder: coordinatesGeocoder,
        container: 'geocoder-container',
        placeholder: 'Choose a type of feature to search for',
        minLength: 1
      }))
      this.geocoder.on('result', this.updateBySearchResult)

      // Add zoom and rotation controls to the map.
      if (!document.getElementById('geocoder').hasChildNodes()) {
        document.getElementById('geocoder')
          .appendChild(this.geocoder.onAdd(this.map))
      }

      this.map.addControl(new mapboxgl.NavigationControl(), 'top-right')
      this.map.addControl(this.draw, 'top-right')
      this.map.addControl(new mapboxgl.ScaleControl(), 'bottom-right')
      this.map.addControl(new mapboxgl.ScaleControl({ unit: 'imperial' }), 'bottom-right')
      this.map.addControl(new mapboxgl.AttributionControl(), 'top-left')
      this.map.addControl(new mapboxgl.GeolocateControl({
        positionOptions: {
          enableHighAccuracy: true
        },
        showUserLocation: false
      }), 'top-right')
      this.map.on('style.load', () => {
        this.getMapLayers()
        this.initStreamHighlights()
      })

      this.initHighlightLayers()
      this.listenForAreaSelect()

      this.lastZoom = this.map.getZoom()

      // special handling for parcels because we may not want to have
      // users turn this layer on/off (it should always be on)
      this.map.on('click', this.setSingleFeature)
      // this.map.on('click', 'parcels', this.setSingleFeature)
      this.map.on('mouseenter', 'parcels', this.setCursorPointer)
      this.map.on('mouseleave', 'parcels', this.resetCursor)

      // NOTE: temporary
      // this.map.on('moveend', this.onMapMoveUpdateStreamLayer)

      // Subscribe to mode change event to toggle drawing state
      this.map.on('draw.modechange', this.handleModeChange)

      // Show layer selection sidebar
      this.$store.commit('toggleInfoPanelVisibility')
    },
    // addShape (shape) {
    //   // adds a mapbox-gl-draw shape to the map
    //   this.map.getSource('customShapeData').setData(shape)
    // },
    // removeShapes () {
    //   this.map.getSource('customShapeData').setData(polygon)
    // },
    // clearSelections () {
    //   this.replaceOldFeatures()
    //   this.$store.commit('clearDataMartFeatures')
    //   this.$store.commit('clearDisplayTemplates')
    //
    //   if (this.dataMartFeatureInfo && this.dataMartFeatureInfo.display_data_name === 'point_of_interest') {
    //     this.$store.commit('resetDataMartFeatureInfo')
    //     this.$store.dispatch('map/clearHighlightLayer')
    //     // EventBus.$emit('highlight:clear')
    //   }
    // },
    handleModeChange (e) {
      if (e.mode === 'draw_polygon' || e.mode === 'draw_point' || e.mode === 'draw_line_string') {
        this.isDrawingToolActive = true
        this.polygonToolHelp()
      } else if (e.mode === 'simple_select') {
        setTimeout(() => {
          this.isDrawingToolActive = false
        }, 500)
      }
    },
    // initHighlightLayers () {
    //   this.map.on('load', () => {
    //     // initialize highlight layer
    //     this.map.addSource('customShapeData', { type: 'geojson', data: polygon })
    //     this.map.addLayer({
    //       'id': 'customShape',
    //       'type': 'fill',
    //       'source': 'customShapeData',
    //       'layout': {},
    //       'paint': {
    //         'fill-color': 'rgba(26, 193, 244, 0.08)',
    //         'fill-outline-color': 'rgb(8, 159, 205)'
    //       }
    //     })
    //     this.map.addSource('highlightLayerData', {
    //       type: 'geojson',
    //       data: polygon
    //     })
    //     this.map.addLayer({
    //       'id': 'highlightLayer',
    //       'type': 'fill',
    //       'source': 'highlightLayerData',
    //       'layout': {},
    //       'paint': {
    //         'fill-color': 'rgba(154, 63, 202, 0.25)'
    //       }
    //     })
    //     this.map.addImage('highlight-point', HighlightPoint(this.map, 90), { pixelRatio: 2 })
    //     this.map.addSource('highlightPointData', { type: 'geojson', data: point })
    //     this.map.addLayer({
    //       'id': 'highlightPoint',
    //       'type': 'symbol',
    //       'source': 'highlightPointData',
    //       'layout': {
    //         'icon-image': 'highlight-point'
    //       }
    //     })
    //   })
    // },
    // initStreamHighlights () {
    //   // Import sources and layers for stream segment highlighting
    //   this.getStreamSources.forEach((s) => {
    //     this.map.addSource(s.name, { type: 'geojson', data: s.options })
    //   })
    //   this.getStreamLayers.forEach((l) => {
    //     this.map.addLayer(l)
    //   })
    // },
    polygonToolHelp () {
      const disableKey = 'disablePolygonToolHelp'
      if (JSON.parse(localStorage.getItem(disableKey)) !== true) {
        EventBus.$emit(
          'help',
          {
            text: 'Draw a polygon by single clicking a series of points. Finish drawing by clicking again on any of the points, or cancel by pressing Escape. The polygon can be cleared by pressing Delete or clicking the trash button.',
            disableKey: disableKey
          })
      }
    },
    // loadLayers () {
    //   const layers = this.allMapLayers
    //
    //   // load each layer, but default to no visibility.
    //   // the user can toggle layers on and off with the layer controls.
    //   for (let i = 0; i < layers.length; i++) {
    //     const layer = layers[i]
    //
    //     // All layers are now vector based sourced from mapbox
    //     // so we don't need to check for layer type anymore
    //     const vector = layer['display_data_name']
    //     // this.map.on('click', vector, this.setSingleFeature)
    //     this.map.on('mouseenter', vector, this.setCursorPointer)
    //     this.map.on('mouseleave', vector, this.resetCursor)
    //   }
    // },
    async updateBySearchResult (data) {
      this.draw.changeMode('simple_select')
      await this.$router.push({ name: 'single-feature' })
      console.log('route changed')
      let lat = data.result.center[1]
      let lng = -Math.abs(data.result.center[0])
      const options = { steps: 10, units: 'kilometers', properties: {} }
      const bounds = circle([lng, lat], 0.01, options) // 10m radius (in km)
      const canvas = this.map.getCanvas()
      const size = { x: canvas.width, y: canvas.height }
      let payload = {
        layers: [{ display_data_name: data.result.layer }],
        bounds: bounds,
        size: size,
        primary_key_match: data.result.primary_id
      }

      this.clearHighlightLayer()
      this.updateHighlightLayerData(data.result)

      if (data.result.place_type === 'coordinate') {
        return
      }

      this.$store.commit('clearDataMartFeatures')
      this.$store.dispatch('map/addMapLayer', data.result.layer)
      this.$store.dispatch('getDataMartFeatures', payload)
    },
    // /*
    //   Highlights a FeatureCollection dataset
    //  */
    // updateHighlightsLayerData (data) {
    //   if (data.display_data_name === 'stream_apportionment') {
    //     this.map.getSource('streamApportionmentSource').setData(data.feature_collection)
    //   }
    // },
    /*
      Highlights a single Feature dataset
     */
    // updateHighlightLayerData (data) {
    //   // For stream networks layer we add custom highlighting and reset poly/point highlight layering
    //   if (data.display_data_name === 'freshwater_atlas_stream_networks') {
    //     this.map.getSource('highlightPointData').setData(point)
    //     this.map.getSource('highlightLayerData').setData(polygon)
    //     console.log('messing with stream highlights')
    //     // For local rendered streams only calculation
    //     this.$store.commit('resetStreamData')
    //     this.updateStreamLayer(data)
    //
    //     // Backend query for all connected streams
    //     // this.$store.dispatch('fetchConnectedStreams', { stream: data })
    //   } else if (data.geometry.type === 'Point') { // Normal poly/point highlighting
    //     this.map.getSource('highlightPointData').setData(data)
    //     this.map.getSource('highlightLayerData').setData(polygon)
    //     this.$store.commit('resetStreamData')
    //     this.$store.commit('resetStreamBufferData')
    //   } else {
    //     this.map.getSource('highlightPointData').setData(point)
    //     this.map.getSource('highlightLayerData').setData(data)
    //     this.$store.commit('resetStreamData')
    //     this.$store.commit('resetStreamBufferData')
    //   }
    // },
    // updateStreamLayer (data) {
    //   let layer = this.map.queryRenderedFeatures({ layers: ['freshwater_atlas_stream_networks'] })
    //   this.$store.dispatch('calculateStreamHighlights', { stream: data, streams: layer })
    // },
    onMapMoveUpdateStreamLayer () {
      if (this.getSelectedStreamData.features) {
        var data = Object.assign({}, this.getSelectedStreamData.features[0])
        const currentZoom = this.map.getZoom()
        if (currentZoom !== this.lastZoom) {
          this.$store.commit('resetStreamData')
          this.$store.commit('resetStreamBufferData')
          this.lastZoom = currentZoom
        }
        this.updateStreamLayer(data)
      }
    },
    // clearHighlightLayer () {
    //   this.map.getSource('highlightPointData').setData(point)
    //   this.map.getSource('highlightLayerData').setData(polygon)
    //   this.$store.commit('resetStreamData')
    //   this.$store.commit('resetStreamBufferData')
    // },
    // handleAddLayer (displayDataName) {
    //   // this.map.setLayoutProperty(displayDataName, 'visibility', 'visible')
    //   this.activateLayer(displayDataName)
    // },
    // handleRemoveLayer (displayDataName) {
    //   this.clearHighlightLayer()
    //   this.map.setLayoutProperty(displayDataName, 'visibility', 'none')
    // },
    // handleAddBaseLayer (layerId) {
    //   this.map.setLayoutProperty(layerId, 'visibility', 'visible')
    // },
    // handleRemoveBaseLayer (layerId) {
    //   this.map.setLayoutProperty(layerId, 'visibility', 'none')
    // },
    // handleAddApiLayer (datamart) {
    //   const layer = this.activeDataMarts.find((x) => {
    //     return x.display_data_name === datamart.displayDataName
    //   })
    //   this.addGeoJSONLayer(layer)
    // },
    // handleRemoveApiLayer (displayDataName) {
    //   this.removeLayer(displayDataName)
    // },
    // addGeoJSONLayer (layer) {
    //   if (!layer || !layer.data) {
    //     console.error('invalid format for data source/data mart')
    //     return
    //   }
    //
    //   // layer.data should have a "features" or "geojson" property, which
    //   // must be a list of geojson Features.  For example, layer.data could be
    //   // a FeatureCollection format object. The 'features' list will be added to the map.
    //   let features
    //   if (layer.data.features && layer.data.features.length) {
    //     features = layer.data.features
    //   } else if (layer.data.geojson && layer.data.geojson.length) {
    //     features = layer.data.geojson
    //   }
    //   if (!features) {
    //     console.error('could not find a features list or object to add to map')
    //     return
    //   }
    //
    //   // this.activeLayers[layer.display_data_name] = L.geoJSON(features, {
    //   //   onEachFeature: function (feature, layer) {
    //   //     layer.bindPopup('<h3>' + feature.properties.name + '</h3><p>' + feature.properties.description + '</p>')
    //   //   }
    //   // })
    //   this.activeLayers[layer.display_data_name].addTo(this.map)
    // },
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
    // removeLayer (layer) {
    //   const displayDataName = layer.display_data_name || layer
    //   if (!displayDataName || !this.activeLayers[displayDataName]) {
    //     return
    //   }
    //   this.map.removeLayer(layer.id)
    //   // delete this.legendGraphics[layer.id]
    //   delete this.activeLayers[layer.id]
    // },
    listenForAreaSelect () {
      this.map.on('draw.create', this.addActiveSelection)
      this.map.on('draw.update', this.addActiveSelection)
    },
    setSingleFeature (e) {
      if (!this.isDrawingToolActive) {
        const scale = MapScale(this.map)
        const radius = scale / 1000 * 0.065 // scale radius based on map zoom level
        const options = { steps: 10, units: 'kilometers', properties: {} }
        const bounds = circle([e.lngLat['lng'], e.lngLat['lat']], radius, options)
        // this.map.getSource('highlightLayerData').setData(bounds) // debug can see search radius
        this.getMapObjects(bounds)
      }
    },
    getPolygonCenter (arr) {
      if (arr.length === 1) {
        return arr
      }
      let x = arr.map(x => x[0])
      let y = arr.map(x => x[1])
      let cx = (Math.min(...x) + Math.max(...x)) / 2
      let cy = (Math.min(...y) + Math.max(...y)) / 2
      return [cx, cy]
    },
    // getArrayDepth (value) {
    //   return Array.isArray(value) ? 1 + Math.max(...value.map(this.getArrayDepth)) : 0
    // },
    formatLatLon (lon, lat) {
      // Formats lat lon to be within proper ranges
      lon = lon < 0 ? lon : -lon
      lat = lat > 0 ? lat : -lat
      return [lon, lat]
    },
    // setCursorPointer () {
    //   this.map.getCanvas().style.cursor = 'pointer'
    // },
    // resetCursor () {
    //   this.map.getCanvas().style.cursor = ''
    // },
    ...mapMutations('map', [
      'setMap',
      'setDraw',
      'setGeocoder',
      'replaceOldFeatures',
      'activateLayer',
      'setCursorPointer',
      'resetCursor'
    ]),
    ...mapActions('map', [
      'clearHighlightLayer',
      'clearSelections',
      'getMapLayers',
      'getMapObjects',
      'addActiveSelection',
      'handleAddPointSelection',
      'initStreamHighlights',
      'initHighlightLayers',
      'updateHighlightLayerData',
      'updateHighlightsLayerData'
    ])
  },
  watch: {
    highlightFeatureData (value) {
      if (value && value.geometry) {
        if (value.geometry.type === 'Point') {
          let coordinates = value.geometry.coordinates
          value.geometry.coordinates = this.formatLatLon(coordinates[0], coordinates[1])
        }
        this.updateHighlightLayerData(value)
      }
    },
    highlightFeatureCollectionData (value) {
      this.updateHighlightsLayerData(value)
    },
    dataMartFeatureInfo (value) {
      if (value && value.geometry) {
        let coordinates = value.geometry.coordinates
        if (value.geometry.type === 'Point') {
          coordinates = this.formatLatLon(coordinates[0], coordinates[1])
          value.geometry.coordinates = coordinates
        } else {
          let depth = getArrayDepth(coordinates)
          let flattened = coordinates.flat(depth - 2)
          coordinates = this.getPolygonCenter(flattened)
        }

        // let flyToCoordinates = [...coordinates]
        // this.map.flyTo({
        //   center: flyToCoordinates
        // })
        this.updateHighlightLayerData(value)
      }
    },
    getSelectedStreamData (value) {
      this.map.getSource(streamConfig.sources[0].name).setData(value)
    },
    getUpstreamData (value) {
      this.map.getSource(streamConfig.sources[1].name).setData(value)
    },
    getDownstreamData (value) {
      this.map.getSource(streamConfig.sources[2].name).setData(value)
    },
    getSelectedStreamBufferData (value) {
      this.map.getSource(streamConfig.sources[3].name).setData(value)
    },
    getUpstreamBufferData (value) {
      this.map.getSource(streamConfig.sources[4].name).setData(value)
    },
    getDownstreamBufferData (value) {
      this.map.getSource(streamConfig.sources[5].name).setData(value)
    }
  }
}
