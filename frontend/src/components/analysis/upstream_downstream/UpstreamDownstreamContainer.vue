<template>
  <v-container class="pt-3">
    <v-toolbar flat>
      <v-banner color="indigo"
                icon="mdi-map-marker"
                icon-color="white"
                width="100%"
      >
        <v-toolbar-title>
          Find features upstream or downstream along a stream
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
    <v-row class="mt-3">
      <v-col class="text-right">
        <v-btn class="ml-3" @click="selectPoint" color="primary" outlined :disabled="buttonClicked">Select a point</v-btn>
      </v-col>
    </v-row>
    <UpstreamDownstream
      :record="selectedStream"
      :coordinates="selectedStream.geometry.coordinates"
      v-if="selectedStream && selectedStream.display_data_name === 'freshwater_atlas_stream_networks'"/>
    <v-row v-else>
      <v-col cols=12>
        <v-card>
          <v-card-title>Instructions</v-card-title>
          <v-card-text>
            <UpstreamDownstreamInstructions></UpstreamDownstreamInstructions>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

import UpstreamDownstream from './UpstreamDownstream'
import UpstreamDownstreamInstructions from './UpstreamDownstreamInstructions'
import ApiService from '../../../services/ApiService'
import qs from 'querystring'

export default {
  name: 'UpstreamDownstreamContainer',
  components: {
    UpstreamDownstream,
    UpstreamDownstreamInstructions
  },
  data: () => ({
    streamsLayerAutomaticallyEnabled: false,
    selectedStream: { geometry: null },
    buttonClicked: false
  }),
  methods: {
    selectPoint () {
      this.setDrawMode('draw_point')
      this.buttonClicked = true
    },
    enableStreamsLayer () {
      this.$store.dispatch('map/addMapLayer', 'freshwater_atlas_stream_networks')
    },
    disableStreamsLayer () {
      this.$store.dispatch('map/removeMapLayer', 'freshwater_atlas_stream_networks')
    },
    resetSelectedStream () {
      this.selectedStream = { geometry: null }
      this.buttonClicked = false
      this.clearSelections()
    },
    ...mapActions(['exitFeature']),
    ...mapActions('map', ['setDrawMode', 'clearSelections'])
  },
  computed: {
    isStreamsLayerEnabled () {
      return this.isMapLayerActive('freshwater_atlas_stream_networks')
    },
    ...mapGetters('map', ['map', 'isMapLayerActive', 'isMapReady']),
    ...mapGetters(['pointOfInterest'])
  },
  watch: {
    isMapReady (value) {
      if (value) {
        if (!this.isStreamsLayerEnabled) {
          this.streamsLayerAutomaticallyEnabled = true
          this.enableStreamsLayer()
        }
      }
    },
    pointOfInterest (value) {
      if (value && value.geometry) {
        this.buttonClicked = false
        const params = {
          point: JSON.stringify(value.geometry.coordinates),
          limit: 1,
          get_all: true,
          with_apportionment: false
        }
        ApiService.query(`/api/v1/streams/nearby?${qs.stringify(params)}`).then((r) => {
          let geojson = r.data.streams[0].geojson
          geojson.display_data_name = 'freshwater_atlas_stream_networks'
          // the nearby endpoint returns values in lower snake case, we capatalize them for consistency
          geojson.properties.LINEAR_FEATURE_ID = geojson.properties.linear_feature_id
          geojson.properties.FWA_WATERSHED_CODE = geojson.properties.fwa_watershed_code
          this.selectedStream = r.data.streams[0].geojson
        }).catch((e) => {
          console.error(e)
        })
      }
    }
  },
  mounted () {
    this.$store.commit('setInfoPanelVisibility', true)
    if (!this.isStreamsLayerEnabled) {
      this.streamsLayerAutomaticallyEnabled = true
      this.enableStreamsLayer()
    }
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
