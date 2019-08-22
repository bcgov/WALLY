import L from 'leaflet'
import { tiledMapLayer } from 'esri-leaflet'
import 'leaflet-lasso'
import 'leaflet-fullscreen/dist/Leaflet.fullscreen.min.js'
import EventBus from '../../services/EventBus.js'
import { mapGetters } from 'vuex'
import betterWms from './L.TileLayer.BetterWMS'
import * as _ from 'lodash'
import { wmsBaseURL } from '../../utils/wmsUtils'
import * as utils from '../../utils/metadataUtils'

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
    // There seems to be an issue loading leaflet immediately on mount, we use nextTick to ensure
    // that the view has been rendered at least once before injecting the map.
    // this.$nextTick(function () {
    this.initLeaflet()
    this.initMap()
    // })

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
    initLeaflet () {
      // There is a known issue using leaflet with webpack, this is a workaround
      // Fix courtesy of: https://github.com/PaulLeCam/react-leaflet/issues/255
      delete L.Icon.Default.prototype._getIconUrl
      L.Icon.Default.mergeOptions({
        iconRetinaUrl: require('../../assets/images/marker-icon-2x.png'),
        iconUrl: require('../../assets/images/marker-icon.png'),
        shadowUrl: require('../../assets/images/marker-shadow.png')
      })
    },
    initMap () {
      this.map = L.map(this.$el, {
        preferCanvas: true,
        minZoom: 4,
        maxZoom: 17
      }).setView([53.8, -124.5], 9)

      L.control.scale().addTo(this.map)
      this.map.addControl(this.getFullScreenControl())
      this.map.addControl(this.getAreaSelectControl())
      // this.map.addControl(this.getLegendControl())
      this.map.addControl(this.getLocateControl())

      // BCGov map tiles
      tiledMapLayer({ url: 'https://maps.gov.bc.ca/arcserver/rest/services/Province/roads_wm/MapServer' }).addTo(this.map)
      // Open Street Map tiles
      // L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      //     maxZoom: 19,
      //     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      // }).addTo(this.map)

      this.activeLayerGroup.addTo(this.map)
      this.markerLayerGroup.addTo(this.map)

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
      console.log('features?', features)
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
      this.activeLayers[layer.id] = betterWms(wmsBaseURL + layer.wmsLayer + '/ows?',
        {
          format: 'image/png',
          layers: 'pub:' + layer.wmsLayer,
          styles: layer.wmsStyle,
          transparent: true,
          name: layer.name,
          overlay: true
        })

      this.activeLayers[layer.id].addTo(this.map)
    },
    removeLayer (layer) {
      const id = layer.id || layer
      if (!id || !this.activeLayers[id]) {
        return
      }
      this.map.removeLayer(this.activeLayers[id])
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
    },
    getMapObjects (bounds) {
      // TODO: Separate activeMaplayers by activeWMSLayers and activeDataMartLayers
      let size = this.map.getSize()
      this.$store.commit('clearDataMartFeatures')
      console.log('active map layers', this.activeMapLayers, this.activeDataMarts)

      this.activeDataMarts.forEach((layer)=>{
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
