<template>
  <div>
    <div id="map" class="map"></div>
    <MapLegend :map="map"></MapLegend>
  </div>
</template>
<style>
    @import "../../../node_modules/mapbox-gl/dist/mapbox-gl.css";
    @import "../../../node_modules/@mapbox/mapbox-gl-draw/dist/mapbox-gl-draw.css";
    @import "../../../node_modules/@mapbox/mapbox-gl-geocoder/dist/mapbox-gl-geocoder.css";
    .map {
        z-index: 2;
        width: 100%;
        height: calc(100vh - 120px);
    }

    .geolocate {
        background-image: url('../../assets/images/geolocate.png');
        width: 30px;
        height: 30px;
        left: 2px;
        box-shadow: 0px 0px 5px 1px rgba(0, 0, 0, 0.4);
        cursor: pointer;
    }

    .geolocate:hover {
        opacity: 0.8;
    }
    .select-box-icon {
        background-image: url('../../assets/images/select-zoom.png');
    }
    .mapboxgl-ctrl-scale:first-child {
      margin-bottom: 0;
    }
    .mapboxgl-ctrl-scale:nth-child(2) {
      border-style: solid solid none;
      border-width: 2px 2px medium;
      margin-top: -2px;
    }
</style>
<script src="./Map.js"></script>
