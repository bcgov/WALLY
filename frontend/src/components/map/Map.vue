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
        width: calc(100vw - 345px);
        height: calc(100vh - 64px);
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
    .mapboxgl-ctrl-geocoder {
        width: 48rem!important;
    }

    .legend {
      background-color: #fff;
      border-radius: 3px;
      bottom: 30px;
      box-shadow: 0 1px 2px rgba(0,0,0,0.10);
      font: 12px/20px 'Helvetica Neue', Arial, Helvetica, sans-serif;
      padding: 10px;
      position: absolute;
      right: 10px;
      z-index: 3;
    }

    .legend h4 {
      margin: 0 0 10px;
    }

    .legend div span {
      border-radius: 50%;
      display: inline-block;
      height: 10px;
      margin-right: 5px;
      width: 10px;
    }

</style>
<script src="./Map.js"></script>
