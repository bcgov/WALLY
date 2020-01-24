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
import { mapGetters } from 'vuex'

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
      if (!this.draw ||
        !this.draw.changeMode ||
        (!newLine && this.dataMartFeatureInfo && this.dataMartFeatureInfo.display_data_name === 'user_defined_line')) {
        return
      }
      this.draw.changeMode('draw_line_string')
    },
    enableWellsLayer () {
      this.$store.commit('addMapLayer', 'groundwater_wells')
    },
    disableWellsLayer () {
      this.$store.commit('removeMapLayer', 'groundwater_wells')
    }
  },
  computed: {
    isWellsLayerEnabled () {
      return this.isMapLayerActive('groundwater_wells')
    },
    ...mapGetters('map', ['draw', 'isMapLayerActive']),
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
    this.draw.changeMode('simple_select')
    if (this.wellsLayerAutomaticallyEnabled) {
      this.disableWellsLayer()
    }
  }
}
</script>

<style>

</style>
