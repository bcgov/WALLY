<template>
  <v-container class="pt-3">
    <v-toolbar flat>
      <v-banner width="100%">
        <v-avatar slot="icon" color="indigo">
          <v-icon
            icon="mdi-vector-line"
            color="white">
            mdi-vector-line
          </v-icon>
        </v-avatar>
        <v-toolbar-title>
          Plot a cross section between wells
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
    <div v-else>
      <v-row class="mt-3">
        <v-col  class="text-right">
          <v-btn @click="drawLine" color="primary" outlined >Draw line</v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols=12 >
          <v-card>
            <v-card-title>Instructions</v-card-title>
            <v-card-text>
              <CrossSectionInstructions></CrossSectionInstructions>
            </v-card-text>
          </v-card>
          <div class="caption" v-if="!isWellsLayerEnabled"><a href="#" @click.prevent="enableWellsLayer">Enable groundwater wells map layer</a></div>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

import WellsCrossSection from './WellsCrossSection.vue'
import CrossSectionInstructions from './CrossSectionInstructions'
export default {
  name: 'CrossSectionContainer',
  components: {
    CrossSectionInstructions,
    WellsCrossSection
  },
  data: () => ({
    wellsLayerAutomaticallyEnabled: false,
    drawClickCount: 0
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
    mapClick (e) {
      if (this.draw && this.draw.getMode) {
        let mode = this.draw.getMode()
        let count = this.drawClickCount
        // Auto-complete cross section line after 2 clicks
        if (mode === 'draw_line_string') {
          if (count === 0) {
            this.drawClickCount += 1
          } else if (count === 1) {
            this.drawClickCount = 0
            this.setDrawMode('simple_select')
          }
        }
      }
    },
    ...mapActions(['exitFeature']),
    ...mapActions('map', ['setDrawMode', 'clearSelections', 'addSelectedFeature'])
  },
  computed: {
    isWellsLayerEnabled () {
      return this.isMapLayerActive('groundwater_wells')
    },
    ...mapGetters('map', ['map', 'draw', 'isMapLayerActive', 'isMapReady']),
    ...mapGetters(['sectionLine'])
  },
  watch: {
    isMapReady (value) {
      if (value) {
        // Check if the URL params contain cross section coordinates. If so,
        // set the point of interest to the section line to display it on app load.
        if (this.$route.query.section_line_A && this.$route.query.section_line_B) {
          const coords = [
            this.$route.query.section_line_A.map(Number),
            this.$route.query.section_line_B.map(Number)
          ]

          const linestring =
            {
              id: 'user_defined_line',
              type: 'Feature',
              geometry: {
                type: 'LineString',
                coordinates: coords
              },
              properties: {
              }
            }

          this.addSelectedFeature(linestring)
        }
        if (!this.isWellsLayerEnabled) {
          this.wellsLayerAutomaticallyEnabled = true
          this.enableWellsLayer()
        }
        this.map.on('click', this.mapClick)
      }
    }
  },
  mounted () {
    if (this.isMapReady) {
      this.clearSelections()
      this.map.on('click', this.mapClick)
    }
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
    this.map.off('click', this.mapClick)
    this.drawClickCount = 0
  }
}
</script>

<style>

</style>
