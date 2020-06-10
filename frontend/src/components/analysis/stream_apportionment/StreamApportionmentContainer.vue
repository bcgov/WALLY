<template>
  <v-container>
    <v-breadcrumbs :items="breadcrumbs">
      <template v-slot:divider>
        <v-icon>mdi-chevron-right</v-icon>
      </template>
    </v-breadcrumbs>
    <v-toolbar flat>
      <v-banner color="indigo"
                icon="mdi-axis-arrow"
                icon-color="white"
                width="100%"
      >
        <v-toolbar-title>
          Stream apportionment
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
      v-if="pointOfInterest &&
            pointOfInterest.display_data_name === 'point_of_interest'">
      <div class="pa-3 mt-3">
        Point at {{ pointOfInterest.geometry.coordinates.map(x => x.toFixed(6)).join(', ') }}
      </div>
      <StreamApportionment
        :record="pointOfInterest"
        />
    </div>

    <v-row class="pa-5" v-else>
      <v-col cols=12 lg=8>
        <p>Zoom into an area of interest on the map.</p>
        <p>
          Click the “Draw Point” button and drop a point of interest to represent a groundwater point of diversion.
          The weighting factor is automatically set to 2 and can be updated after your analysis is produced.
          The weighting factor must be either 1 (linear) or 2 (squared).
        </p>
        <p>
          After your analysis is produced, there are buttons available to: remove multiple streams, remove overlaps,
          and remove streams where apportionment is less than 10%. Each row in the table has an eye icon to highlight
          stream segments and a trash can icon to delete that specific stream segment. If you have made modifications
          to your analysis, a counterclockwise arrow icon will appear beside the weighting factor - click on this
          button to reset the analysis to the initial results.
        </p>
        <p>
          You can export results to Excel by selecting the “Excel” button.
        </p>
          If no analysis is produced, then go to the drop down Selection menu in the top navigation bar and
          "Reset Selections" and try again. It also helps to have the map zoomed to a smaller area with a
          sufficiently large amount of detail.
        <p>
          For more information on what data is used and caveats to the analysis, please review the
          "Where does this information come from?" box at the bottom of the page.
        </p>
      </v-col>
      <v-col class="text-right"><v-btn @click="selectPoint" color="primary" outlined>Draw point</v-btn></v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

import StreamApportionment from './StreamApportionment.vue'

export default {
  name: 'StreamApportionmentContainer',
  components: {
    StreamApportionment
  },
  data: () => ({
    streamsLayerAutomaticallyEnabled: false,
    breadcrumbs: []
  }),
  methods: {
    selectPoint () {
      this.setDrawMode('draw_point')
    },
    enableStreamsLayer () {
      this.$store.dispatch('map/addMapLayer', 'freshwater_atlas_stream_networks')
    },
    disableStreamsLayer () {
      this.$store.dispatch('map/removeMapLayer', 'freshwater_atlas_stream_networks')
    },
    loadApportionment () {
      if (!this.isStreamsLayerEnabled) {
        this.streamsLayerAutomaticallyEnabled = true
        this.enableStreamsLayer()
      }
      this.setBreadcrumbs()
      this.loadFeature()
    },
    setBreadcrumbs () {
      if (this.$route.query.coordinates) {
        this.breadcrumbs = [{
          text: 'Home',
          disabled: false,
          to: { path: '/' }
        },
        {
          text: 'Point of Interest',
          disabled: false,
          to: {
            path: '/point-of-interest',
            query: { coordinates: this.$route.query.coordinates.map((x) => x) }
          }
        }, {
          text: 'Stream apportionment',
          disabled: true
        }]
      }
    },
    loadFeature () {
      if ((!this.pointOfInterest || !this.pointOfInterest.geometry) && this.$route.query.coordinates) {
        // load feature from coordinates
        const coordinates = this.$route.query.coordinates.map((x) => Number(x))

        let data = {
          coordinates: coordinates,
          layerName: 'point-of-interest'
        }

        this.$store.dispatch('map/addFeaturePOIFromCoordinates', data)
      }
    },
    ...mapActions(['exitFeature']),
    ...mapActions('map', ['setDrawMode', 'clearSelections'])
  },
  computed: {
    isStreamsLayerEnabled () {
      return this.isMapLayerActive('freshwater_atlas_stream_networks')
    },
    ...mapGetters('map', ['draw', 'isMapLayerActive', 'isMapReady']),
    ...mapGetters(['pointOfInterest'])
  },
  watch: {
    isMapReady (value) {
      if (value) {
        this.loadApportionment()
      }
    }
  },
  mounted () {
    this.clearSelections()
    this.$store.commit('setInfoPanelVisibility', true)
    this.loadApportionment()
  },
  beforeDestroy () {
    if (this.streamsLayerAutomaticallyEnabled) {
      this.disableStreamsLayer()
    }
  }
}
</script>

<style>

</style>
