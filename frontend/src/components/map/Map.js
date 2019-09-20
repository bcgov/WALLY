import MapLegend from './MapLegend.vue'
import EventBus from '../../services/EventBus.js'
import { mapGetters, mapActions } from 'vuex'
import * as _ from 'lodash'
import { wmsBaseURL } from '../../utils/wmsUtils'
import mapboxgl from 'mapbox-gl'
import MapboxDraw from '@mapbox/mapbox-gl-draw'
import MapboxGeocoder from '@mapbox/mapbox-gl-geocoder'
import DrawRectangle from 'mapbox-gl-draw-rectangle-mode'

import bbox from '@turf/bbox'

import qs from 'querystring'
import ApiService from '../../services/ApiService'

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

    // this.$store.dispatch(FETCH_DATA_LAYERS)
  },
  beforeDestroy () {
    EventBus.$off('layer:added', this.handleAddWMSLayer)
    EventBus.$off('layer:removed', this.handleRemoveWMSLayer)
    EventBus.$off('dataMart:added', this.handleAddApiLayer)
    EventBus.$off('dataMart:removed', this.handleRemoveApiLayer)
    EventBus.$off('feature:added', this.handleAddFeature)
    EventBus.$off('layers:loaded', this.loadLayers)
  },
  data () {
    return {
      map: null,
      // legendControlContent: null,
      // activeLayerGroup: L.layerGroup(),
      // markerLayerGroup: L.layerGroup(),
      activeLayers: {},
      draw: null // mapbox draw object (controls drawn polygons e.g. for area select)
    }
  },
  computed: {
    ...mapGetters([
      'allMapLayers',
      'activeMapLayers',
      'allDataMarts',
      'activeDataMarts'
    ])
  },
  methods: {
    initMap () {
      // temporary read token with limited scope (reading layers) just for
      // testing.
      mapboxgl.accessToken = `pk.eyJ1IjoiaWl0LXdhdGVyIiwiYSI6ImNrMHI2NjlibTAyODkzbW93Y3R3amd4bTkifQ.rve1IbrClbRJotzQ5-m_8Q`

      this.map = new mapboxgl.Map({
        container: 'map', // container id
        style: 'mapbox://styles/iit-water/ck0pm9gqz6qiw1cnxrf9s8yu2', // stylesheet location
        center: [-124, 54.5], // starting position
        zoom: 4.7 // starting zoom
      })

      const modes = MapboxDraw.modes
      modes.draw_polygon = DrawRectangle

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
      this.map.addControl(geocoder, 'top-left')
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

      this.listenForAreaSelect()

      // special handling for parcels because we may not want to have
      // users turn this layer on/off (it should always be on)
      this.map.on('click', 'parcels', this.setSingleFeature)
      this.map.on('mouseenter', 'parcels', this.setCursorPointer)
      this.map.on('mouseleave', 'parcels', this.resetCursor)
    },
    loadLayers () {
      const layers = this.allMapLayers

      // load each layer, but default to no visibility.
      // the user can toggle layers on and off with the layer controls.
      for (let i = 0; i < layers.length; i++) {
        const layer = layers[i]

        // layers are either vector, WMS, or geojson.
        // they are loading differently depending on the type.
        if (layer['vector_name']) {
          const vector = layer['vector_name']
          this.map.on('click', vector, this.setSingleFeature)
          this.map.on('mouseenter', vector, this.setCursorPointer)
          this.map.on('mouseleave', vector, this.resetCursor)
        } else if (layer['wms_name']) {
          // console.log('adding wms layer ', layers[i].display_data_name)
          this.addWMSLayer(layer)
        } else if (layer['geojson']) {
          this.addGeoJSONLayer(layer)
        }
      }
    },
    async searchWallyAPI () {
      const results = await ApiService.getApi('/geocode?q=a')
      console.log(results.data)
      return results.data
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
    addWMSLegendGraphic (layername, style) {
      const wmsOpts = {
        service: 'WMS',
        request: 'GetLegendGraphic',
        format: 'image/png',
        layer: 'pub:' + layername,
        style: style,
        transparent: true,
        name: layername,
        height: 20,
        width: 20,
        overlay: true,
        srs: 'EPSG:3857'
      }

      const query = qs.stringify(wmsOpts)
      const url = wmsBaseURL + layer.wms_name + '/ows?' + query
      this.legendGraphics[layerID] = url

    },
    replaceOldFeatures (newFeature) {
      // replace all previously drawn features with the new one.
      // this has the effect of only allowing one selection box to be drawn at a time.
      const old = this.draw.getAll().features.filter((f) => f.id !== newFeature)
      this.draw.delete(old.map((feature) => feature.id))
    },
    handleSelect (feature) {
      const newFeature = feature.features[0].id
      this.replaceOldFeatures(newFeature)

      // for drawn rectangular regions, the polygon describing the rectangle is the first
      // element in the array of drawn features.
      const bounds = bbox(feature.features[0])
      this.getMapObjects(bounds)
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
      const id = e.features[0].id
      const coordinates = e.features[0].geometry.coordinates.slice()
      const properties = e.features[0].properties

      this.$store.commit('setDataMartFeatureInfo',
        {
          display_data_name: id,
          coordinates: coordinates,
          properties: properties
        })
    },
    setCursorPointer () {
      this.map.getCanvas().style.cursor = 'pointer'
    },
    resetCursor () {
      this.map.getCanvas().style.cursor = ''
    },
    ...mapActions(['getMapLayers'])
    // listenForReset () {
    //     this.$parent.$on('resetLayers', (data) => {
    //         if (this.map) {
    //             this.map.eachLayer((layer) => {
    //                 if (layer.wmsParams && layer.wmsParams.overlay) {
    //                     this.map.removeLayer(layer)
    //                 }
    //             })
    //             this.map.setView([54.5, -126.5], 5)
    //         }
    //     })
    // },
  }
}
