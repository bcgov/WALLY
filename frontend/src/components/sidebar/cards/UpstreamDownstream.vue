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
    <StreamBufferData
      :record="dataMartFeatureInfo"
      :coordinates="dataMartFeatureInfo.geometry.coordinates"
      v-if="dataMartFeatureInfo && dataMartFeatureInfo.display_data_name === 'point_of_interest'"/>
    <div class="pa-5" v-else>
      <p>Select a point on a stream to view water data upstream and downstream.</p>
    </div>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'

import StreamBufferData from '../../analysis/StreamBufferData'

export default {
  name: 'UpstreamDownstream',
  components: {
    StreamBufferData
  },
  data: () => ({
    streamsLayerAutomaticallyEnabled: false
  }),
  methods: {
    selectPoint () {
      if (this.draw && this.draw.changeMode) {
        this.draw.changeMode('draw_point')
      }
    },
    enableStreamsLayer () {
      this.$store.dispatch('map/addMapLayer', 'freshwater_atlas_stream_networks')
    },
    disableStreamsLayer () {
      this.$store.commit('map/removeMapLayer', 'freshwater_atlas_stream_networks')
    }
  },
  computed: {
    ...mapGetters('map', ['draw', 'isMapLayerActive']),
    ...mapGetters(['dataMartFeatureInfo'])
  },
  mounted () {
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
