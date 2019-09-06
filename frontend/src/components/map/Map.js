import L from 'leaflet'
import 'leaflet-lasso'
import 'leaflet-fullscreen/dist/Leaflet.fullscreen.min.js'
import EventBus from '../../services/EventBus.js'
import { mapGetters, mapActions } from 'vuex'
import * as _ from 'lodash'
import { wmsBaseURL } from '../../utils/wmsUtils'
import * as utils from '../../utils/metadataUtils'

import mapboxgl from 'mapbox-gl'
import MapboxDraw from '@mapbox/mapbox-gl-draw'
import DrawRectangle from 'mapbox-gl-draw-rectangle-mode'

import bbox from '@turf/bbox'

import qs from 'querystring'

// Extend control, making a locate
L.Control.Locate = L.Control.extend({
  onAdd: function (map) {
    let container = L.DomUtil.create('div', 'geolocate')
    L.DomEvent.addListener(container, 'click', this.click, this)
    return container
  },
  onRemove: function (map) {

  },
  click: function (ev) {
    // Use callback to handle clicks
    if (this.onClick) {
      this.onClick(ev)
    }
  }
})
L.control.locate = function (opts) {
  return new L.Control.Locate(opts)
}

export default {
  name: 'WallyMap',
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
      activeLayerGroup: L.layerGroup(),
      markerLayerGroup: L.layerGroup(),
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
      // this.map = L.map(this.$el, {
      //   preferCanvas: true,
      //   minZoom: 4,
      //   maxZoom: 17
      // }).setView([54, -124], 5)

      // L.control.scale().addTo(this.map)
      // this.map.addControl(this.getFullScreenControl())
      // this.map.addControl(this.getAreaSelectControl())
      // // this.map.addControl(this.getLegendControl())
      // this.map.addControl(this.getLocateControl())

      // // BCGov map tiles
      // tiledMapLayer({ url: 'https://maps.gov.bc.ca/arcserver/rest/services/Province/roads_wm/MapServer' }).addTo(this.map)
      // // Open Street Map tiles
      // // L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      // //     maxZoom: 19,
      // //     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      // // }).addTo(this.map)

      // this.activeLayerGroup.addTo(this.map)
      // this.markerLayerGroup.addTo(this.map)

      // temporary public token with limited scope (reading layers) just for testing.
      mapboxgl.accessToken = `pk.eyJ1Ijoic3RlcGhlbmhpbGxpZXIiLCJhIjoiY2p6encxamxnMjJldjNjbWxweGthcHFneCJ9.y5h99E-kHzFQ7hywIavY-w`

      this.map = new mapboxgl.Map({
        container: 'map', // container id
        style: 'mapbox://styles/stephenhillier/cjzydtam02lbd1cld4jbkqlhy', // stylesheet location
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

      // Add zoom and rotation controls to the map.
      this.map.addControl(new mapboxgl.NavigationControl(), 'top-left')
      this.map.addControl(this.draw, 'top-left')

      this.map.on('style.load', () => {
        this.getMapLayers()
      })

      this.listenForAreaSelect()
    },
    loadLayers () {
      const layers = this.allMapLayers

      // load each layer, but default to no visibility.
      // the user can toggle layers on and off with the layer controls.
      for (let i = 0; i < layers.length; i++) {
        const layer = layers[i]
        if (layer['wms_name']) {
          console.log('adding wms layer ', layers[i].display_data_name)
          this.addWMSLayer(layer)
        } else if (layer['geojson']) {
          this.addGeoJSONLayer(layer)
        }
      }
    },
    getLocateControl () {
      const locateButton = L.control.locate({ position: 'topleft' })
      locateButton.onClick = (ev) => {
        this.map.locate({ setView: true, maxZoom: 12 })
      }
      return locateButton
    },
    getFullScreenControl () {
      return new L.Control.Fullscreen({
        position: 'topleft'
      })
    },
    getAreaSelectControl () {
      const lasso = L.lasso(this.map)
      return new (L.Control.extend({
        options: {
          position: 'topleft'
        },
        onAdd: function (map) {
          let container = L.DomUtil.create('div', 'leaflet-bar leaflet-control')
          container.innerHTML = '<a class="leaflet-bar-part leaflet-bar-part-single select-box-icon"></a>'
          container.onclick = function (map) {
            lasso.enable()
          }
          return container
        }
      }))()
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
      console.log(displayDataName)
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

      this.activeLayers[layer.display_data_name] = L.geoJSON(features, {
        onEachFeature: function (feature, layer) {
          layer.bindPopup('<h3>' + feature.properties.name + '</h3><p>' + feature.properties.description + '</p>')
        }
      })
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
        styles: layer.wmsStyle,
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
        },
        'paint': {}
      }
      this.activeLayers[layerID] = newLayer
      this.map.addLayer(newLayer, 'wells')
    },
    removeLayer (layer) {
      const displayDataName = layer.display_data_name || layer
      if (!displayDataName || !this.activeLayers[displayDataName]) {
        return
      }
      this.map.removeLayer(layer.id)
      delete this.activeLayers[layer.id]
    },
    // getLegendControl () {
    //   const self = this
    //   return new (L.Control.extend({
    //     options: {
    //       position: 'bottomright'
    //     },
    //     onAdd (map) {
    //       const container = L.DomUtil.create('div', 'leaflet-control-legend')
    //       const content = L.DomUtil.create('div', 'leaflet-control-legend-content')
    //       self.legendControlContent = content
    //       content.innerHTML = `<div class="m-1">Legend</div>`
    //       container.appendChild(content)
    //       return container
    //     }
    //   }))()
    // },
    replaceOldFeatures (newFeature) {
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
