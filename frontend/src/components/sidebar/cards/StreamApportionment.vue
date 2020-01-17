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

    <div class="pa-5" v-else>
      <p>Select a point of interest (e.g. a proposed well site) to apportion demand to nearby streams.</p>
      <v-btn v-if="noPointSelected" @click="selectPoint" color="secondary" tile outlined>Select point of interest</v-btn>
    </div>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'

import StreamApportionment from '../../analysis/StreamApportionment'

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
      if (this.draw && this.draw.changeMode) {
        this.draw.changeMode('draw_point')
      }
    },
    enableStreamsLayer () {
      this.$store.commit('addMapLayer', 'freshwater_atlas_stream_networks')
    },
    disableStreamsLayer () {
      this.$store.commit('removeMapLayer', 'freshwater_atlas_stream_networks')
    }
  },
  computed: {
    noPointSelected () {
      if (this.draw && this.draw.getMode !== 'draw_point' &&
         this.dataMartFeatureInfo && this.dataMartFeatureInfo.display_data_name !== 'point_of_interest') {
        return true
      }
      return false
    },
    isStreamsLayerEnabled () {
      return this.isMapLayerActive('freshwater_atlas_stream_networks')
    },
    ...mapGetters('map', ['draw', 'isMapLayerActive']),
    ...mapGetters(['dataMartFeatureInfo'])
  },
  mounted () {
    if (!this.isStreamsLayerEnabled) {
      this.streamsLayerAutomaticallyEnabled = true
      this.enableStreamsLayer()
    }

    if (!this.dataMartFeatureInfo || this.dataMartFeatureInfo.display_data_name !== 'point_of_interest') {
      this.selectPoint()
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
