import MapLegend from './MapLegend.vue'
import EventBus from '../../services/EventBus.js'
import { mapGetters, mapActions, mapMutations } from 'vuex'
import mapboxgl from 'mapbox-gl'
import MapboxGeocoder from '@mapbox/mapbox-gl-geocoder'
import MapScale from './MapScale'
import circle from '@turf/circle'
import coordinatesGeocoder from './localGeocoder'

import { getArrayDepth } from '../../helpers'

import ApiService from '../../services/ApiService'

export default {
  name: 'Map',
  components: { MapLegend },
  mounted () {
    this.initMap()
  },
  beforeDestroy () {
  },
  data () {
    return {
      lastZoom: 6,
      activeLayers: {}
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
      'geocoder',
      'isDrawingToolActive'
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
      await this.$store.dispatch('map/initMapAndDraw')

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
      await this.$store.dispatch('map/loadMap')
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
      this.map.on('draw.modechange', this.setDrawToolInActive)

      // Show layer selection sidebar
      // this.$store.commit('toggleInfoPanelVisibility')
    },
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
    async updateBySearchResult (data) {
      this.setDrawMode('simple_select')
      await this.$router.push({ name: 'single-feature' })
      global.config.debug && console.log('[wally] route changed')
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
      await this.$store.dispatch('map/addMapLayer', data.result.layer)
      await this.$store.dispatch('getDataMartFeatures', payload)
    },
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
    loadLayers (layers) {
      // load each layer, but default to no visibility.
      // the user can toggle layers on and off with the layer controls.
      for (let i = 0; i < layers.length; i++) {
        const layer = layers[i]

        // All layers are now vector based sourced from mapbox
        // so we don't need to check for layer type anymore
        const layerName = layer['display_data_name']
        // we use a custom cursor for stream selection so we dont set the cursor for it
        if (layerName !== 'freshwater_atlas_stream_networks') {
          this.map.on('mouseenter', layerName, this.setCursorPointer)
          this.map.on('mouseleave', layerName, this.resetCursor)
        }
      }
    },
    listenForAreaSelect () {
      this.map.on('draw.create', (fc) => this.addActiveSelection({ featureCollection: fc, options: { alwaysReplaceFeatures: true } }))
      this.map.on('draw.update', (fc) => this.addActiveSelection({ featureCollection: fc, options: { alwaysReplaceFeatures: true } }))
    },
    setSingleFeature (e) {
      if (!this.isDrawingToolActive) {
        const scale = MapScale(this.map)
        const radius = scale / 1000 * 0.065 // scale radius based on map zoom level
        const options = { steps: 10, units: 'kilometers', properties: {} }
        const bounds = circle([e.lngLat['lng'], e.lngLat['lat']], radius, options)

        // this.map.getSource('highlightLayerData').setData(bounds) // debug can see search radius
        this.getMapObjects({ bounds })
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
    formatLatLon (lon, lat) {
      // Formats lat lon to be within proper ranges
      lon = lon < 0 ? lon : -lon
      lat = lat > 0 ? lat : -lat
      return [lon, lat]
    },
    ...mapMutations('map', [
      'setMap',
      'setDraw',
      'setGeocoder',
      'replaceOldFeatures',
      'activateLayer',
      'setCursorPointer',
      'resetCursor',
      'setDrawToolInActive'
    ]),
    ...mapActions('map', [
      'clearHighlightLayer',
      'clearSelections',
      'getMapLayers',
      'getMapObjects',
      'addActiveSelection',
      'handleAddPointSelection',
      'initHighlightLayers',
      'updateHighlightLayerData',
      'updateHighlightsLayerData',
      'setDrawMode'
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
    // highlightFeatureCollectionData (value) {
    //   this.updateHighlightsLayerData(value)
    // },
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
    allMapLayers (value) {
      if (value) {
        this.loadLayers(value)
      }
    }
  }
}
