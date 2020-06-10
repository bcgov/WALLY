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
    <v-row class="mx-3 mt-4">
      <v-col cols=12 lg=8>
        <p>Select a point on a stream to view water data upstream and downstream.</p>

        <p>
          Zoom into an area of interest on the map.
        </p>
        <p>
          Click on the "Select Point" button and select a point on a stream. The buffer radius is
          automatically set to 50 metres and can be updated from 0 to 500 metres after your analysis is produced.
        </p>
        <p>
          You can search the entire upstream catchment or within the distance of the stream. The entire
          upstream catchment is the full area that drains to the point you selected (entire drainage basin
          upstream from your point). The stream buffer shows the area within the buffer radius from the stream.
        </p>
        <p>
          A drop down menu gives you options of layers to analyze: Groundwater Wells, Water Rights Licences,
          Water Rights Applications, EcoCat Reports, Aquifers or Critical Habitats. After you make a selection,
          there is the option to enable the layer to see all the features of that layer.
        </p>
        <p>
          If no analysis is produced, then go to the drop down Selection menu in the top navigation bar and
          "Reset Selections" and try again. It also helps to have the map zoomed to a smaller area with a
          sufficiently large amount of detail.
        </p>
        <p>
          For more information on what data is used and caveats to the analysis, please review the "Where does
          this information come from?" box at the bottom of the page.
        </p>
      </v-col>
      <v-col class="text-right">
        <v-btn class="ml-3" @click="selectPoint" color="primary" outlined :disabled="buttonClicked">Select Point</v-btn>
      </v-col>
    </v-row>
    <FeatureStreamBuffer
      :record="selectedStream"
      :coordinates="selectedStream.geometry.coordinates"
      v-if="selectedStream && selectedStream.display_data_name === 'freshwater_atlas_stream_networks'"/>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

import FeatureStreamBuffer from '../../features/FeatureStreamBuffers'
import ApiService from '../../../services/ApiService'
import qs from 'querystring'

export default {
  name: 'UpstreamDownstream',
  components: {
    FeatureStreamBuffer
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
