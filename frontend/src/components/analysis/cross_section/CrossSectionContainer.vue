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
      <v-col cols=12 lg=10>
        <v-card outlined>
          <v-card-title>Instructions</v-card-title>
          <v-card-text>
            <p>Zoom into a place of interest on the map.</p>
            <p>Click on the "Draw a Line" button and draw a line on the map, which can be a straight line through an
              area of wells or can be segmented to connect different wells. Double click to complete the line.
              The buffer radius is automatically set to 200 metres and can be updated to 0 to 1000 metres after
              your analysis is produced.</p>
            <p>If no analysis is produced, then go to the drop down Selection menu and "Reset Selections" and try again. It also helps to have the map zoomed to a smaller area with a sufficiently large amount of detail.</p>
            <p>When you hover over the resulting 2D and 3D graphs, a toolbar of icons will appear. To view lithology, select the box or lasso icon and then create a box or lasso over the wells in the graph that you want to see the lithology for.</p>
            <p>The table below the graph displays the wells in your buffer radius. If you do not want a well included in your analysis, then click on the trash icon in the corresponding row and it will be removed from the graph and analysis.</p>
            <p>Select the Excel button to download the data and information related to the wells within your cross section.</p>
          </v-card-text>
        </v-card>
<!--        <p>Draw a line to plot a cross section of subsurface data.</p>-->
        <div class="caption" v-if="!isWellsLayerEnabled"><a href="#" @click.prevent="enableWellsLayer">Enable groundwater wells map layer</a></div>
      </v-col>
      <v-col class="text-right" lg=2>
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
