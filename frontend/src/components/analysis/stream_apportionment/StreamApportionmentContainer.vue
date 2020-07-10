<template>
  <v-container class="pt-3">
    <v-breadcrumbs v-if="breadcrumbs && breadcrumbs.length" :items="breadcrumbs">
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
          Assign demand from a well to hydraulically connected streams
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
      <StreamApportionment
        :record="pointOfInterest"
        />
    </div>

    <v-row v-else class="mt-3">
      <v-col class="text-right"><v-btn @click="selectPoint" color="primary" outlined>Draw point</v-btn></v-col>
      <v-col cols=12>
        <v-card>
          <v-card-title>Instructions</v-card-title>
          <v-card-text>
            <StreamApportionmentInstructions></StreamApportionmentInstructions>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

import StreamApportionment from './StreamApportionment.vue'
import StreamApportionmentInstructions from './StreamApportionmentInstructions'
export default {
  name: 'StreamApportionmentContainer',
  components: {
    StreamApportionment,
    StreamApportionmentInstructions
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
            query: { coordinates: this.$route.query.coordinates }
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
