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
    v-if="sectionLine && sectionLine.display_data_name === 'user_defined_line'">
      <WellsCrossSection
      :record="sectionLine"
      :coordinates="sectionLine.geometry.coordinates"
      @crossSection:redraw="() => drawLine({ newLine: true })"
      />

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

import WellsCrossSection from './WellsCrossSection'
export default {
  name: 'CrossSectionContainer',
  components: {
    WellsCrossSection
  },
  data: () => ({
    wellsLayerAutomaticallyEnabled: false
  }),
  methods: {
    drawLine (options = {}) {
      const newLine = options.newLine || false
      if (!newLine && this.sectionLine && this.sectionLine.display_data_name === 'user_defined_line') {
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
    ...mapActions(['exitFeature']),
    ...mapActions('map', ['setDrawMode', 'clearSelections'])
  },
  computed: {
    isWellsLayerEnabled () {
      return this.isMapLayerActive('groundwater_wells')
    },
    ...mapGetters('map', ['draw', 'isMapLayerActive', 'isMapReady']),
    ...mapGetters(['sectionLine'])
  },
  watch: {
    isMapReady (value) {
      if (value) {
        if (!this.isWellsLayerEnabled) {
          this.wellsLayerAutomaticallyEnabled = true
          this.enableWellsLayer()
        }
      }
    }
  },
  mounted () {
    this.clearSelections()
    this.$store.commit('setInfoPanelVisibility', true)
    if (!this.isWellsLayerEnabled) {
      this.wellsLayerAutomaticallyEnabled = true
      this.enableWellsLayer()
    }
  },
  beforeDestroy () {
    if (this.wellsLayerAutomaticallyEnabled) {
      this.disableWellsLayer()
    }
  }
}
</script>

<style>

</style>
