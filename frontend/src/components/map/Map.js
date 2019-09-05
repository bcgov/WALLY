import L from 'leaflet'
import 'leaflet-lasso'
import 'leaflet-fullscreen/dist/Leaflet.fullscreen.min.js'
import EventBus from '../../services/EventBus.js'
import { mapGetters } from 'vuex'
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

    // this.$store.dispatch(FETCH_DATA_LAYERS)
  },
  beforeDestroy () {
    EventBus.$off('layer:added', this.handleAddWMSLayer)
    EventBus.$off('layer:removed', this.handleRemoveWMSLayer)
    EventBus.$off('dataMart:added', this.handleAddApiLayer)
    EventBus.$off('dataMart:removed', this.handleRemoveApiLayer)
    EventBus.$off('feature:added', this.handleAddFeature)
  },
  data () {
    return {
      map: null,
      // legendControlContent: null,
      activeLayerGroup: L.layerGroup(),
      markerLayerGroup: L.layerGroup(),
      activeLayers: {}
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

      var draw = new MapboxDraw({
        modes: modes,
        displayControlsDefault: false,
        controls: {
          polygon: true,
          trash: true
        }
      })

      // Add zoom and rotation controls to the map.
      this.map.addControl(new mapboxgl.NavigationControl(), 'top-left')
      this.map.addControl(draw, 'top-left')

      this.listenForAreaSelect()
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
    handleAddWMSLayer (layerId) {
      const layer = this.allMapLayers.find((x) => { // TODO Handle Data Sources (Data Marts) here as well
        return x.id === layerId
      })
      // stop if layer wasn't found in the array we searched
      if (!layer) {
        return
      }
      // inspect the layer to determine how to load it
      if (layer['wmsLayer']) {
        this.addWMSLayer(layer)
      } else if (layer['geojson']) {
        this.addGeoJSONLayer(layer)
      }
    },
    handleRemoveWMSLayer (layerId) {
      const layer = this.allMapLayers.find((x) => {
        return x.id === layerId
      })
      this.removeLayer(layer)
    },
    handleAddApiLayer (datamart) {
      const layer = this.activeDataMarts.find((x) => {
        return x.id === datamart.id
      })
      this.addGeoJSONLayer(layer)
    },
    handleRemoveApiLayer (id) {
      this.removeLayer(id)
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

      this.activeLayers[layer.id] = L.geoJSON(features, {
        onEachFeature: function (feature, layer) {
          layer.bindPopup('<h3>' + feature.properties.name + '</h3><p>' + feature.properties.description + '</p>')
        }
      })
      this.activeLayers[layer.id].addTo(this.map)
    },
    addWMSLayer (layer) {
      if (!layer.id || !layer.wmsLayer || !layer.name) {
        return
      }

      const wmsOpts = {
        service: 'WMS',
        request: 'GetMap',
        format: 'image/png',
        layers: 'pub:' + layer.wmsLayer,
        styles: layer.wmsStyle,
        transparent: true,
        name: layer.name,
        height: 256,
        width: 256,
        overlay: true,
        srs: 'EPSG:3857'
      }

      const query = qs.stringify(wmsOpts)
      const url = wmsBaseURL + layer.wmsLayer + '/ows?' + query + '&BBOX={bbox-epsg-3857}'

      const newLayer = {
        'id': layer.id,
        'type': 'raster',
        'source': {
          'type': 'raster',
          'tiles': [
            url
          ],
          'tileSize': 256
        },
        'paint': {}
      }
      this.activeLayers[layer.id] = newLayer

      // TODO: this should only happen once (on map load?)
      // layer visibility should be toggled, not adding/removing layers.
      this.map.addLayer(newLayer, 'aeroway-line')
    },
    removeLayer (layer) {
      const id = layer.id || layer
      if (!id || !this.activeLayers[id]) {
        return
      }
      this.map.removeLayer(id)
      delete this.activeLayers[id]
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
    listenForAreaSelect () {
      this.map.on('lasso.finished', (event) => {
        let lats = event.latLngs.map(l => l.lat)
        let lngs = event.latLngs.map(l => l.lng)

        let min = L.latLng(Math.min(...lats), Math.min(...lngs))
        let max = L.latLng(Math.max(...lats), Math.max(...lngs))
        let bounds = [min.lng, min.lat, max.lng, max.lat].join(',')

        this.getMapObjects(bounds)
      })

      this.map.on('draw.create', (feature) => {
        // for drawn rectangular regions, the polygon describing the rectangle is the first
        // element in the array of drawn features.
        const bounds = bbox(feature.features[0])
        this.getMapObjects(bounds)
      })
    },
    getMapObjects (bounds) {
      // TODO: Separate activeMaplayers by activeWMSLayers and activeDataMartLayers
      const canvas = this.map.getCanvas()
      const size = { x: canvas.width, y: canvas.height }

      this.$store.commit('clearDataMartFeatures')
      console.log('active map layers', this.activeMapLayers, this.activeDataMarts)

      this.activeDataMarts.forEach((layer) => {
        console.log('datamart layer?', layer, layer.id)
        layer.data.features.forEach(feature => {
          this.$store.dispatch('getDataMartFeatures', { type: utils.API_DATAMART, layer: layer.id, feature: feature })
        })
      })
      this.activeMapLayers.forEach((layer) => {
        console.log('what layer?', layer)
        this.$store.dispatch('getDataMartFeatures', { type: utils.WMS_DATAMART, bounds: bounds, size: size, layer: layer.wmsLayer })
      })
    }
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
