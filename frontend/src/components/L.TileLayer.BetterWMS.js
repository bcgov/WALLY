import * as L from "leaflet";
import ApiService from "../services/ApiService";
import {round} from "lodash";
import {SET_SINGLE_MAP_OBJECT_SELECTION} from "../store/map/mutations.types"
import store from "../store"

L.TileLayer.BetterWMS = L.TileLayer.WMS.extend({

    onAdd: function (map) {
        // Triggered when the layer is added to a map.
        //   Register a click listener, then do all the upstream WMS things
        L.TileLayer.WMS.prototype.onAdd.call(this, map);
        map.on('click', this.getFeatureInfo, this);
    },

    onRemove: function (map) {
        // Triggered when the layer is removed from a map.
        //   Unregister a click listener, then do all the upstream WMS things
        L.TileLayer.WMS.prototype.onRemove.call(this, map);
        map.off('click', this.getFeatureInfo, this);
    },

    getFeatureInfo: function (evt) {
        // Make an AJAX request to the server and hope for the best
        let url = this.getFeatureInfoUrl(evt.latlng)
        let showResults = L.Util.bind(this.showGetFeatureInfo, this);
        ApiService.getRaw(url).then((response) => {
            showResults(evt.latlng, response.data);
        }).catch((error) => {
            showResults(error);
        })
    },

    getFeatureInfoUrl: function (latlng) {
        // Construct a GetFeatureInfo request URL given a point
        var point = this._map.latLngToContainerPoint(latlng, this._map.getZoom()),
            size = this._map.getSize(),

            params = {
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
                info_format: 'text/html'
            };

        params[params.version === '1.3.0' ? 'i' : 'x'] = round(point.x);
        params[params.version === '1.3.0' ? 'j' : 'y'] = round(point.y);

        return this._url + L.Util.getParamString(params, this._url, true);
    },

    showGetFeatureInfo: function (latlng, content) {
        // if (err) { console.log(err); return; } // do nothing if there's an error

        // this._map.removeLayer(this.point)
        // Otherwise show the content in a popup, or something.
        store.commit(SET_SINGLE_MAP_OBJECT_SELECTION, content)
        // this.point = L.point(40,40).setLatLng(latlng).addTo(this._map)
        // L.popup({ maxWidth: 800})
        //     .setLatLng(latlng)
        //     .setContent(content)
        //     .openOn(this._map);
    }
});

export default function (url, options) {
    return new L.TileLayer.BetterWMS(url, options);
};
