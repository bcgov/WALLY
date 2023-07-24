<template>
  <v-container class="pt-5">
    <v-toolbar flat>
      <v-banner width="100%">
        <v-avatar slot="icon" color="indigo">
          <v-icon
            icon="mdi-shape-polygon-plus"
            color="white">
            mdi-shape-polygon-plus
          </v-icon>
        </v-avatar>
        <v-toolbar-title>Measuring distance and area</v-toolbar-title>
      </v-banner>
    </v-toolbar>
    <v-row class="pa-5">
      <v-col>
        <p>Zoom into an area of interest on the map. To measure distance, click once to start to draw a line and then double click to complete the line.</p>
        <p>To measure perimeter and area, ensure your last double click point is near your first click point to finish your polygon.</p>
      </v-col>
      <v-col class="text-right">
        <v-col>
          <v-btn @click="selectDrawLine" color="primary" outlined>Draw a line or polygon</v-btn>
        </v-col>
        <v-col>
          <v-btn @click="clearLine" color="primary" outlined>Clear</v-btn>
        </v-col>
      </v-col>
    </v-row>
    <v-row v-if="drawnMeasurements">
      <v-col cols="12">
      <v-card>
        <v-card-title class="subheading font-weight-bold">Measurements</v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <p v-if="drawnMeasurements.distance"><strong>Distance:</strong> {{drawnMeasurements.distance}}</p>
          <p v-if="drawnMeasurements.perimeter"><strong>Perimeter:</strong> {{drawnMeasurements.perimeter}}</p>
          <p v-if="drawnMeasurements.area"><strong>Area:</strong> {{drawnMeasurements.area}}</p>
        </v-card-text>
      </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from 'vuex'
export default {
  name: 'MeasuringTool',
  data: () => ({
    buttonClicked: false,
    distance: 0,
    area: 0
  }),
  methods: {
    selectDrawLine () {
      this.setDrawMode('draw_line_string')
    },
    clearLine () {
      this.clearSelections()
    },
    ...mapActions('map', ['setDrawMode', 'clearSelections', 'updateMeasurementHighlight']),
    ...mapMutations('map', ['setMode'])
  },
  computed: {
    ...mapGetters('map', ['draw', 'drawnMeasurements']),
    ...mapGetters(['dataMartFeatures'])
  },
  watch: {
    drawnMeasurements (value) {
      if (value && value.feature) {
        this.updateMeasurementHighlight(value)
      }
    }
  },
  mounted () {
    this.setMode({ type: 'analyze', name: 'measuring_tool' })
  },
  beforeDestroy () {
    this.setMode({ type: 'interactive', name: '' })
  }
}
</script>

<style>
</style>
