<template>
    <div id="map" class="map"/>
</template>

<script>
    /* tslint:disable */
    import L from 'leaflet'
    import { tiledMapLayer } from 'esri-leaflet'
    import { filter } from 'lodash'
    import { GeoSearchControl, EsriProvider } from 'leaflet-geosearch'
    import 'leaflet-lasso'
    import 'leaflet-fullscreen/dist/Leaflet.fullscreen.min.js'
    import ArtesianLegend from '../assets/images/artesian.png'
    import CadastralLegend from '../assets/images/cadastral.png'
    import EcocatWaterLegend from '../assets/images/ecocat-water.png'
    import GWaterLicenceLegend from '../assets/images/gwater-licence.png'
    import OWellsInactiveLegend from '../assets/images/owells-inactive.png'
    import OWellsActiveLegend from '../assets/images/owells-active.png'
    import WellsAllLegend from '../assets/images/wells-all.png'
    import Supercluster from 'supercluster'
    import ApiService from "../services/ApiService";

    import { mapGetters } from 'vuex';
    import betterWms from '../components/L.TileLayer.BetterWMS'
    import {FETCH_DATA_SOURCES, FETCH_MAP_OBJECTS, CLEAR_MAP_SELECTIONS} from '../store/map/actions.types'

    const provider = new EsriProvider()
    const searchControl = new GeoSearchControl({
        provider: provider,
        autoClose: true
    })


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
            this.$nextTick(function () {
                this.initLeaflet()
                this.initMap()
            })

            this.$store.dispatch(FETCH_DATA_SOURCES)
        },
        data () {
            return {
                map: null,
                legendControlContent: null,
                layerControls: null,
                mapLayers: null,
                wells: [],
                wellMarkers: null,
                wellMarkersLayerGroup: L.layerGroup(),
                activeLayerGroup: L.layerGroup(),
                markerLayerGroup: L.layerGroup()
            }
        },
        computed: {
            ...mapGetters([
                'externalDataSources',
                'activeMapLayers',
                'mapLayerSelections',
                'mapLayerSingleSelection'])
        },
        watch: {
            wells: function (newWells, oldWells) {
                if (this.map) {
                    this.map.eachLayer((layer) => {
                        if (layer.options.type === 'wellMarkers') {
                            this.map.removeLayer(layer)
                        }
                    })
                    this.addWellsToMap(newWells)
                }
            },
            activeMapLayers: function(newLayers, oldLayers) { // remove and re-add the new main layergroup
                this.map.removeLayer(this.activeLayerGroup)
                this.activeLayerGroup = L.layerGroup(this.buildActiveLayers()).addTo(this.map)
            },
            mapLayerSingleSelection: function (newSelection, oldSelection) {
                // this.map.removeLayer(this.markerLayerGroup)
                // this.markerLayerGroup = L.layerGroup()
                // L.marker(newSelection.point).addTo(this.markerLayerGroup).addTo(this.map)
                let p = newSelection.point
                if(p) {
                    L.popup()
                        .setLatLng(p)
                        .setContent(p.toString())
                        .openOn(this.map);
                }
            },
            mapLayerSelections: function (newSelections, oldSelections) {
                if(typeof (this.mapLayerSelections) == 'Array') {
                    this.mapLayerSelections.forEach((selection) => {
                        selection.forEach((point) => {
                            L.marker(L.latlng(point.coordinates)).addTo(this.markerLayerGroup)
                        })
                    })
                    this.markerLayerGroup.addTo(this.map)
                }
            }
        },
        methods: {
            initLeaflet () {
                // There is a known issue using leaflet with webpack, this is a workaround
                // Fix courtesy of: https://github.com/PaulLeCam/react-leaflet/issues/255
                delete L.Icon.Default.prototype._getIconUrl
                L.Icon.Default.mergeOptions({
                    iconRetinaUrl: require('../assets/images/marker-icon-2x.png'),
                    iconUrl: require('../assets/images/marker-icon.png'),
                    shadowUrl: require('../assets/images/marker-shadow.png')
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
                // this.map.addControl(searchControl)
                this.map.addControl(this.getAreaSelectControl())
                // this.map.addControl(this.getLegendControl())
                this.map.addControl(this.getLocateControl())

                // Add map layers.
                // tiledMapLayer({ url: 'https://maps.gov.bc.ca/arcserver/rest/services/Province/roads_wm/MapServer' }).addTo(this.map)
                tiledMapLayer({ url: 'https://maps.gov.bc.ca/arcserver/rest/services/Province/roads_wm/MapServer' }).addTo(this.map)
                // L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                //     maxZoom: 19,
                //     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                // }).addTo(this.map)
                this.activeLayerGroup.addTo(this.map)
                this.markerLayerGroup.addTo(this.map)


                // L.geoJSON(this.externalDataSources.features, {
                //     onEachFeature: function (feature, layer) {
                //         layer.bindPopup('<h3>'+feature.properties.name+'</h3><p><a href="'+feature.properties.web_uri+'" target="_blank">Web link</a></p>');
                //     }
                // }).addTo(this.map)

                // this.layerControls = L.control.layers(null, this.toggleLayers(), {collapsed: false}).addTo(this.map)

                // this.listenForLayerToggle()
                // this.listenForLayerAdd()
                // this.listenForLayerRemove()
                // this.listenForMapMovement()
                // this.listenForReset()
                this.listenForAreaSelect()


            },
            getLocateControl () {
                const locateButton = L.control.locate({ position: 'topleft' })
                locateButton.onClick = (ev) => {
                    this.map.locate({setView: true, maxZoom: 12})
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
                        var container = L.DomUtil.create('div', 'leaflet-bar leaflet-control')
                        container.innerHTML = '<a class="leaflet-bar-part leaflet-bar-part-single select-box-icon"></a>'
                        container.onclick = function (map) {
                            lasso.enable()
                        }
                        return container
                    }
                }))()
            },
            getLegendControl () {
                const self = this
                return new (L.Control.extend({
                    options: {
                        position: 'bottomright'
                    },
                    onAdd (map) {
                        const container = L.DomUtil.create('div', 'leaflet-control-legend')
                        const content = L.DomUtil.create('div', 'leaflet-control-legend-content')
                        self.legendControlContent = content
                        content.innerHTML = `<div class="m-1">Legend</div>`
                        container.appendChild(content)
                        return container
                    }
                }))()
            },
            // listenForLayerToggle () {
            //     this.$on('activeLayers', (data) => {
            //         let innerContent = `<ul class="p-0 m-0" style="list-style-type: none;">`
            //         innerContent += `<li class="m-1 text-center">Legend</li>`
            //         data.map(l => {
            //             innerContent += `<li class="m-1"><img src="${l.legend}"> ${l.layerName}</li>`
            //         })
            //         innerContent += `</ul>`
            //         this.legendControlContent.innerHTML = innerContent
            //     })
            // },
            listenForAreaSelect () {
                this.map.on('lasso.finished', (event) => {
                    let lats = event.latLngs.map(l => l.lat)
                    let lngs = event.latLngs.map(l => l.lng)

                    let min = L.latLng(Math.min(...lats), Math.min(...lngs))
                    let max = L.latLng(Math.max(...lats), Math.max(...lngs))
                    let bounds = [min.lng, min.lat, max.lng, max.lat].join(',')

                    console.log(bounds)
                    this.getMapObjects(bounds)
                })
            },
            getMapObjects (bounds) {
                let size = this.map.getSize()

                this.$store.dispatch(CLEAR_MAP_SELECTIONS)
                this.activeMapLayers.forEach((layer) => {
                    this.$store.dispatch(FETCH_MAP_OBJECTS, {bounds: bounds, size: size, layer: layer.wmsLayer})
                })
                // for(layer of this.activeMapLayers) {
                //     this.$store.dispatch(FETCH_MAP_OBJECTS, {bounds: bounds, size: size, layer: layer})
                // }
                // for (let [key, value] of Object.entries(this.activeMapLayers)) {
                //     if(value) {
                //         this.$store.dispatch(FETCH_MAP_OBJECTS, {bounds: bounds, size: size, layer: key})
                //     }
                // }
            },
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
            getFeaturesOnMap (map) {
                const layersInBound = []
                const bounds = map.getBounds()
                map.eachLayer((layer) => {
                    if (layer.feature && bounds.overlaps(layer.getBounds())) {
                        layersInBound.push(layer)
                    }
                })
                return layersInBound
            },
            listenForMapMovement () {
                const events = ['zoomend', 'moveend']
                events.map(eventName => {
                    this.map.on(eventName, (e) => {
                        const map = e.target
                        // const layersInBound = this.getFeaturesOnMap(map)
                        // this.$parent.$emit('featuresOnMap', layersInBound)
                        this.updateMapObjects(map)
                    })
                })
            },
            addAquifersToMap (aquifers) {
                const self = this
                function popUpLinkHandler (e) {
                    let routeData = self.$router.resolve({
                        name: 'aquifers-view',
                        params: {
                            id: this.id
                        }
                    })
                    window.open(routeData.href, '_blank')
                }
                function getPopUp (aquifer) {
                    const container = L.DomUtil.create('div', 'leaflet-popup-aquifer')
                    const popUpLink = L.DomUtil.create('div', 'leaflet-popup-link')
                    popUpLink.innerHTML = `<p>Aquifer ID: <span class="popup-link">${aquifer.id}</span></p>
          <p>Aquifer name: ${aquifer.name || ''}</p>
          <p>Aquifer subtype: ${aquifer.subtype || ''}</p>`
                    L.DomEvent.on(popUpLink, 'click', popUpLinkHandler.bind(aquifer))
                    container.appendChild(popUpLink)
                    return container
                }
                if (aquifers !== undefined && aquifers.constructor === Array && aquifers.length > 0) {
                    var myStyle = {
                        'color': 'purple'
                    }
                    aquifers = aquifers.filter((a) => a.gs)
                    aquifers.forEach(aquifer => {
                        L.geoJSON(aquifer.gs, {
                            aquifer_id: aquifer['id'],
                            style: myStyle,
                            type: 'geojsonfeature',
                            onEachFeature: function (feature, layer) {
                                layer.bindPopup(getPopUp(aquifer))
                            }
                        }).addTo(this.map)
                    })
                }
            },
            zoomToSelectedAquifer (data) {
                if (this.map) {
                    this.map.eachLayer((layer) => {
                        if ((layer.options.aquifer_id === data.id) && layer.feature) {
                            this.$nextTick(function () {
                                layer.openPopup()
                            })
                        }
                    })
                }
                var aquiferGeom = L.geoJSON(data.gs)
                this.map.fitBounds(aquiferGeom.getBounds())
                this.$SmoothScroll(document.getElementById('map'))
            },

            // L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW/ows?', {
            //     format: 'image/png',
            //     layers: 'pub:WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW',
            //     styles: 'PMBC_Parcel_Fabric_Cadastre_Outlined',
            //     transparent: true
            // }).addTo(this.map)
            //
            // // Aquifer outlines
            // L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW/ows?', {
            //     format: 'image/png',
            //     layers: 'pub:WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW',
            //     transparent: true
            // }).addTo(this.map)

            buildActiveLayers () {
                let layers = []
                this.activeMapLayers.forEach((layer) => {
                    layers.push(
                        betterWms("https://openmaps.gov.bc.ca/geo/pub/" + layer.wmsLayer + "/ows?",
                            {
                                format: 'image/png',
                                layers: 'pub:' + layer.wmsLayer,
                                styles: layer.wmsStyle,
                                transparent: true,
                                name: layer.name,
                                overlay: true
                            })
                    )
                })
                return layers

                // return {
                // 'Artesian wells': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW/ows?', {
                //     format: 'image/png',
                //     layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
                //     styles: 'Water_Wells_Artesian',
                //     transparent: true,
                //     name: 'Artesian wells',
                //     legend: ArtesianLegend,
                //     overlay: true
                // }),
                // 'Water Rights Licenses': betterWms('https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.WLS_WATER_RIGHTS_LICENCES_SV/ows?', {
                //     format: 'image/png',
                //     layers: 'pub:WHSE_WATER_MANAGEMENT.WLS_WATER_RIGHTS_LICENCES_SV',
                //     transparent: true,
                //     name: 'Water rights licenses',
                //     legend: ArtesianLegend,
                //     overlay: true
                // }),
                // 'Cadastral': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW/ows?', {
                //     format: 'image/png',
                //     layers: 'pub:WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW',
                //     transparent: true,
                //     name: 'Cadastral',
                //     legend: CadastralLegend,
                //     overlay: true
                // }),
                // 'Ecocat - Water related reports': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_FISH.ACAT_REPORT_POINT_PUB_SVW/ows?', {
                //     format: 'image/png',
                //     layers: 'pub:WHSE_FISH.ACAT_REPORT_POINT_PUB_SVW',
                //     transparent: true,
                //     name: 'Ecocat - Water related reports',
                //     legend: EcocatWaterLegend,
                //     overlay: true
                // }),
                // 'Groundwater licences': betterWms('https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.WLS_PWD_LICENCES_SVW/ows?', {
                //     format: 'image/png',
                //     layers: 'pub:WHSE_WATER_MANAGEMENT.WLS_PWD_LICENCES_SVW',
                //     transparent: true,
                //     name: 'Groundwater licences',
                //     legend: GWaterLicenceLegend,
                //     overlay: true
                // }),
                // 'Observation wells - active': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW/ows?', {
                //     format: 'image/png',
                //     layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
                //     styles: 'Provincial_Groundwater_Observation_Wells_Active',
                //     transparent: true,
                //     name: 'Observation wells - active',
                //     legend: OWellsActiveLegend,
                //     overlay: true
                // }),
                // 'Observation wells - inactive': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW/ows?', {
                //     format: 'image/png',
                //     layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
                //     styles: 'Provincial_Groundwater_Observation_Wells_Inactive',
                //     transparent: true,
                //     name: 'Observation wells - inactive',
                //     legend: OWellsInactiveLegend,
                //     overlay: true
                // }),
                // 'Wells - All': L.tileLayer.wms('https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW/ows?', {
                //     format: 'image/png',
                //     layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
                //     transparent: true,
                //     name: 'Wells - All',
                //     legend: WellsAllLegend,
                //     overlay: true
                // }),
                // 'Wells - All': this.wellMarkersLayerGroup
                // }
            }
        }
    }
</script>
<style>
    @import '~leaflet-geosearch/assets/css/leaflet.css';
    @import '~leaflet-fullscreen/dist/leaflet.fullscreen.css';
    @import "~leaflet/dist/leaflet.css";
    .map {
        width: 100%;
        height: calc(100vh - 64px);
    }
    .leaflet-control-geosearch a.reset {
        display: none;
    }

    .leaflet-areaselect-shade {
        position: absolute;
        background: rgba(0,0,0, 0.4);
    }
    .leaflet-areaselect-handle {
        position: absolute;
        background: #fff;
        border: 1px solid #666;
        -moz-box-shadow: 1px 1px rgba(0,0,0, 0.2);
        -webkit-box-shadow: 1px 1px rgba(0,0,0, 0.2);
        box-shadow: 1px 1px rgba(0,0,0, 0.2);
        width: 14px;
        height: 14px;
        cursor: move;
    }
    .geolocate {
        background-image: url('../assets/images/geolocate.png');
        width: 30px;
        height: 30px;
        left: 2px;
        box-shadow: 0px 0px 5px 1px rgba(0, 0, 0, 0.4);
        cursor: pointer;
    }

    .leaflet-control-address {
        width: 30px;
        height: 30px;
        left: 2px;
        box-shadow: 0px 0px 5px 1px rgba(0, 0, 0, 0.4);
        cursor: pointer;
        background-color: white;
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
    }
    .geolocate:hover {
        opacity: 0.8;
    }
    .select-box-icon {
        background-image: url('../assets/images/select-zoom.png');
    }

    .leaflet-popup-link .popup-link {
        text-decoration: underline !important;
        color: #37598A !important;
        cursor: pointer;
    }

    .leaflet-control-legend {
        background-color: white;
        box-shadow: 0px 0px 5px 1px rgba(0, 0, 0, 0.4);
        border-radius: 0.1em;
    }
</style>
