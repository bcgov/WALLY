import * as L from 'leaflet'
import { round } from 'lodash'
import store from '../../store'

L.TileLayer.BetterWMS = L.TileLayer.WMS.extend({

  onAdd: function (map) {
    // Triggered when the layer is added to a map.
    //   Register a click listener, then do all the upstream WMS things
    L.TileLayer.WMS.prototype.onAdd.call(this, map)
    map.on('click', this.getFeatureInfo, this)
  },

  onRemove: function (map) {
    // Triggered when the layer is removed from a map.
    //   Unregister a click listener, then do all the upstream WMS things
    L.TileLayer.WMS.prototype.onRemove.call(this, map)
    map.off('click', this.getFeatureInfo, this)
  },

  getFeatureInfo: function (evt) {
    let url = this.getFeatureInfoUrl(evt.latlng)
    store.dispatch('getFeatureInfo', { url: url, lat: evt.latlng.lat, lng: evt.latlng.lng })
  },

  getFeatureInfoUrl: function (latlng) {
    // Construct a GetFeatureInfo request URL given a point
    var point = this._map.latLngToContainerPoint(latlng, this._map.getZoom())
    var size = this._map.getSize()

    var params = {
      request: 'GetFeatureInfo',
      service: 'WMS',
      srs: 'EPSG:4326',
      styles: this.wmsParams.styles,
      transparent: this.wmsParams.transparent,
      version: this.wmsParams.version,
      format: this.wmsParams.format,
      bbox: this._map.getBounds().toBBoxString(),
      height: size.y,
      width: size.x,
      layers: this.wmsParams.layers,
      query_layers: this.wmsParams.layers,
      info_format: 'application/json'
    }

    params[params.version === '1.3.0' ? 'i' : 'x'] = round(point.x)
    params[params.version === '1.3.0' ? 'j' : 'y'] = round(point.y)

    return this._url + L.Util.getParamString(params, this._url, true)
  }

})

export default function (url, options) {
  return new L.TileLayer.BetterWMS(url, options)
};
