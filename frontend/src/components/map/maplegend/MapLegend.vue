<template>
  <div v-if="Object.keys(legend).length > 0" id="legend" class="legend">
    <div class="legendItems" v-show="show">
      <div v-for="(layer, i) in legend" v-bind:key="`layer${i}`">
        <div v-if="layer.display_data_name.startsWith('fish_observations')">
          <FishObservationsLegendItem :layer=layer />
        </div>
        <div v-else-if="layer.display_data_name === 'water_licensed_works'">
          <WaterLicensedWorksLegendItem :item="getLegendItem(layer)" />
        </div>
        <div v-else-if="layer.display_data_name === 'water_rights_licences'">
          <WaterRightsLicencesLegendItem :item="getLegendItem(layer)" />
        </div>
        <div v-else-if="layer.display_data_name === 'water_approval_points'">
          <WaterApprovalPointsLegendItem :item="getLegendItem(layer)" />
        </div>
        <div v-else-if="layer.display_data_name === 'streams_with_water_allocation_notations'">
          <StreamAllocationNotationsLegendItem :item="getLegendItem(layer)" />
        </div>
        <div v-else-if="excludedLayers.includes(layer.display_data_name)">
          <!-- render nothing for these layers -->
        </div>
        <div v-else>
          <LegendItem :item="getLegendItem(layer)" />
        </div>
      </div>

    </div>
    <v-tooltip left>
      <template v-slot:activator="{ on }">
        <v-btn icon v-on="on" @click="toggle" x-small class="float-right close">
          <v-icon v-if="show">mdi-close</v-icon>
          <v-icon v-else>mdi-map-legend</v-icon>
        </v-btn>
      </template>
      <span v-if="show">Hide</span>
      <span v-else>Show map legend</span>
    </v-tooltip>
  </div>
</template>

<style>
  .legend {
    background-color: #fff;
    border-radius: 3px;
    bottom: 60px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.10);
    font-size: 12px;
    line-height: 20px;
    padding: 10px;
    position: absolute;
    right: 10px;
    z-index: 3;
  }

  .legendItems {
    /* Don't cover the other map tools at the top right*/
    max-height: calc(100vh - 380px);
    overflow: auto;
  }

  .legend h4 {
    margin: 10px 0 0 0;
    font-weight: normal;
    font-style: italic;
  }

  .legend div span {
    display: inline-block;
    height: 10px;
    margin-right: 5px;
    margin-left: 5px;
  }

  .legend .v-icon {
    width: 20px;
  }

  .legend .img {
    width: 20px;
  }

  .legend .grouped {
    margin-left: 20px;
  }
</style>
<script src="./MapLegend.js"></script>
