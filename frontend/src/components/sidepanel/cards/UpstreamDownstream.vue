<template>
  <v-container class="pt-5">
    <v-toolbar flat>
      <v-banner color="indigo"
                icon="mdi-map-marker"
                icon-color="white"
                width="100%"
      >
        <v-toolbar-title>
          Find features along a stream
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
    <FeatureStreamBuffer
      :record="selectedStream"
      :coordinates="selectedStream.geometry.coordinates"
      v-if="selectedStream && selectedStream.display_data_name === 'freshwater_atlas_stream_networks'"/>
    <div class="pa-5" v-else>
      <p>Select a point on a stream to view water data upstream and downstream.</p>
    </div>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

import FeatureStreamBuffer from '../../features/FeatureStreamBuffers'

export default {
  name: 'UpstreamDownstream',
  components: {
    FeatureStreamBuffer
  },
  data: () => ({
    streamsLayerAutomaticallyEnabled: false,
    selectedStream: { geometry: null }
  }),
  methods: {
    enableStreamsLayer () {
      this.$store.dispatch('map/addMapLayer', 'freshwater_atlas_stream_networks')
    },
    disableStreamsLayer () {
      this.$store.dispatch('map/removeMapLayer', 'freshwater_atlas_stream_networks')
    },
    ...mapActions(['exitFeature'])
  },
  computed: {
    isStreamsLayerEnabled () {
      return this.isMapLayerActive('freshwater_atlas_stream_networks')
    },
    ...mapGetters('map', ['draw', 'isMapLayerActive', 'isMapReady']),
    ...mapGetters(['dataMartFeatureInfo'])
  },
  watch: {
    isMapReady (value) {
      console.log('ud ismapready', value)
      if (value) {
        this.draw.changeMode('simple_select')

        if (!this.isStreamsLayerEnabled) {
          this.streamsLayerAutomaticallyEnabled = true
          this.enableStreamsLayer()
        }
      }
    },
    dataMartFeatureInfo (value) {
      if (value && value.display_data_name === 'freshwater_atlas_stream_networks') {
        this.selectedStream = value
      } else {
        // Reset the dataMartFeatureInfo to the current selected stream
        this.$store.commit('setDataMartFeatureInfo', this.selectedStream)
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
