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

    <UpstreamDownstream
      :point="selectedPoint"
      v-if="selectedPoint"/>
    <div v-else>
    <v-row class="mt-3">
      <v-col class="text-right">
        <v-btn class="ml-3" @click="selectPoint" color="primary" outlined :disabled="buttonClicked">Select a point</v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols=12>
        <v-card>
          <v-card-title>Instructions</v-card-title>
          <v-card-text>
            <UpstreamDownstreamInstructions></UpstreamDownstreamInstructions>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    </div>

  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

import UpstreamDownstream from './UpstreamDownstream'
import UpstreamDownstreamInstructions from './UpstreamDownstreamInstructions'

export default {
  name: 'UpstreamDownstreamContainer',
  components: {
    UpstreamDownstream,
    UpstreamDownstreamInstructions
  },
  data: () => ({
    streamsLayerAutomaticallyEnabled: false,
    selectedPoint: '',
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
    ...mapActions(['exitFeature']),
    ...mapActions('map', ['setDrawMode'])
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
        this.selectedPoint = JSON.stringify(value.geometry.coordinates)
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
