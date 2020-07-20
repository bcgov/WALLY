<template>
  <v-container class="pt-5">
    <v-toolbar flat>
      <v-banner color="indigo" icon="mdi-shape-polygon-plus" icon-color="white" width="100%">
        <v-toolbar-title>Measuring distance and area</v-toolbar-title>
      </v-banner>
    </v-toolbar>
    <v-row class="pa-5">
      <v-col cols="12" lg="8">
        <p>Zoom into an area of interest on the map and draw a line to view the distance and area.</p>
      </v-col>
      <v-col class="text-right">
        <v-btn @click="selectDrawLine" color="primary" outlined :disabled="buttonClicked">Draw line</v-btn>
        <v-btn @click="clearLine" class="mx-2" color="primary" outlined>Clear</v-btn>
      </v-col>
    </v-row>
    <v-row v-if="drawnMeasurements.distance">
      <v-col cols="12">
      <v-card>
        <v-card-title class="subheading font-weight-bold">Measurements</v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <p><b>Distance:</b> {{drawnMeasurements.distance}}</p>
          <p><b>Area:</b> {{drawnMeasurements.area}}</p>
        </v-card-text>
      </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
export default {
  name: "MeasuringTool",
  data: () => ({
    buttonClicked: false,
    distance: 0,
    area: 0
  }),
  methods: {
    selectDrawLine() {
      this.setDrawMode("draw_line_string");
      // this.buttonClicked = true;
    },
    clearLine() {
      this.clearSelections()
    },
    ...mapActions("map", ["setDrawMode", "clearSelections"])
  },
  computed: {
    ...mapGetters("map", ["draw", "drawnMeasurements"]),
    ...mapGetters(["dataMartFeatures"])
  },
  watch: {
    drawnMeasurements (value) {
      if (value && value.features && value.features.length > 0) {
        console.log(value)
      }
    }
  },
  mounted() {},
  beforeDestroy() {}
};
</script>

<style>
</style>
