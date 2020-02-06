<template>
  <v-container class="pt-5">
    <v-toolbar flat>
      <v-banner color="indigo"
                icon="mdi-vector-line"
                icon-color="white"
                width="100%"
      >
        <v-toolbar-title>
          Cross section
        </v-toolbar-title>
      </v-banner>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
        <v-btn icon v-on="on" v-on:click="exitFeature">
          <v-icon>close</v-icon>
        </v-btn>
        </template>
        <span>Exit</span>
      </v-tooltip>
    </v-toolbar>
    <div
    v-if="dataMartFeatureInfo && dataMartFeatureInfo.display_data_name === 'user_defined_line'">
      <WellsCrossSection
      :record="dataMartFeatureInfo"
      :coordinates="dataMartFeatureInfo.geometry.coordinates"
      />
      <v-btn @click="() => drawLine({ newLine: true })" color="primary" outlined class="mt-5">Draw new line</v-btn>
    </div>

    <v-row class="pa-5" v-else>
      <v-col cols=12 lg=8>
        <p>Draw a line to plot a cross section of subsurface data.</p>
        <div class="caption" v-if="!isWellsLayerEnabled"><a href="#" @click.prevent="enableWellsLayer">Enable groundwater wells map layer</a></div>
      </v-col>
      <v-col class="text-right">
        <v-btn @click="drawLine" color="primary" outlined>Draw line</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

import WellsCrossSection from '../../analysis/WellsCrossSection'

export default {
  name: 'DrawCrossSection',
  components: {
    WellsCrossSection
  },
  data: () => ({
    wellsLayerAutomaticallyEnabled: false
  }),
  methods: {
    drawLine (options = {}) {
      const newLine = options.newLine || false
      if (!newLine && this.dataMartFeatureInfo && this.dataMartFeatureInfo.display_data_name === 'user_defined_line') {
        return
      }
      this.setDrawMode('draw_line_string')
    },
    enableWellsLayer () {
      this.$store.dispatch('map/addMapLayer', 'groundwater_wells')
    },
    disableWellsLayer () {
      this.$store.dispatch('map/removeMapLayer', 'groundwater_wells')
    },
    exitFeature () {
      this.$store.dispatch('map/clearSelections')
      this.$router.push('/')
    },
    ...mapActions('map', ['setDrawMode'])
  },
  computed: {
    isWellsLayerEnabled () {
      return this.isMapLayerActive('groundwater_wells')
    },
    ...mapGetters('map', ['isMapLayerActive']),
    ...mapGetters(['dataMartFeatureInfo'])
  },
  mounted () {
    this.drawLine()
    if (!this.isWellsLayerEnabled) {
      this.wellsLayerAutomaticallyEnabled = true
      this.enableWellsLayer()
    }
  },
  beforeDestroy () {
    if (this.wellsLayerAutomaticallyEnabled) {
      this.disableWellsLayer()
    }
    this.$store.dispatch('map/clearSelections')
  }
}
</script>

<style>

</style>
