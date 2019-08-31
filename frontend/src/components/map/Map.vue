<template>
    <div id="map" class="map"></div>
</template>
<style>
    /* @import '../../../node_modules/leaflet-geosearch/assets/css/leaflet.css';
    @import '../../../node_modules/leaflet-fullscreen/dist/leaflet.fullscreen.css'; */
    @import "../../../node_modules/mapbox-gl/dist/mapbox-gl.css";
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
        background-image: url('../../assets/images/geolocate.png');
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
        background-image: url('../../assets/images/select-zoom.png');
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
<script src="./Map.js"></script>
