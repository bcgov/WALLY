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
    </v-toolbar>
    <FeatureStreamBuffer
      :record="dataMartFeatureInfo"
      :coordinates="dataMartFeatureInfo.geometry.coordinates"
      v-if="dataMartFeatureInfo && dataMartFeatureInfo.display_data_name === 'freshwater_atlas_stream_networks'"/>
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
    streamsLayerAutomaticallyEnabled: false
  }),
  methods: {
    enableStreamsLayer () {
      this.$store.dispatch('map/addMapLayer', 'freshwater_atlas_stream_networks')
    },
    disableStreamsLayer () {
      this.$store.dispatch('map/removeMapLayer', 'freshwater_atlas_stream_networks')
    },
    ...mapActions('map', ['setDrawMode'])
  },
  computed: {
    isStreamsLayerEnabled () {
      return this.isMapLayerActive('freshwater_atlas_stream_networks')
    },
    ...mapGetters('map', ['isMapLayerActive', 'isMapReady']),
    ...mapGetters(['dataMartFeatureInfo'])
  },
  watch: {
    isMapReady (value) {
      if (value) {
        this.setDrawMode('simple_select')

        if (!this.isStreamsLayerEnabled) {
          this.streamsLayerAutomaticallyEnabled = true
          this.enableStreamsLayer()
        }
      }
    }
  },
  mounted () {
    this.map && this.map.on('load', () => {

    })
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
