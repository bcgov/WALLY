<template>
  <v-container class="pt-5">
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
    </v-toolbar>
    <div
      v-if="dataMartFeatureInfo &&
            dataMartFeatureInfo.display_data_name === 'point_of_interest'">
      <div class="pa-3 mt-3">
        Point at {{ dataMartFeatureInfo.geometry.coordinates.map(x => x.toFixed(6)).join(', ') }}
      </div>
      <StreamApportionment
        :record="dataMartFeatureInfo"
        />
    </div>

    <v-row class="pa-5" v-else>
      <v-col cols=12 lg=8><p>Select a point of interest (e.g. a proposed well site) to apportion demand to nearby streams.</p></v-col>
      <v-col class="text-right"><v-btn @click="selectPoint" color="primary" outlined>Draw point</v-btn></v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

import StreamApportionment from '../../analysis/StreamApportionment.vue'

export default {
  name: 'StreamApportionmentStart',
  components: {
    StreamApportionment
  },
  data: () => ({
    streamsLayerAutomaticallyEnabled: false
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
    ...mapActions('map', ['setDrawMode'])
  },
  computed: {
    isStreamsLayerEnabled () {
      return this.isMapLayerActive('freshwater_atlas_stream_networks')
    },
    ...mapGetters('map', ['isMapLayerActive']),
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
