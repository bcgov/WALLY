<template>
  <v-sheet class="pa-5">
    <div class="title my-3">
          Selected Stream: {{streamName}}
    </div>
      <v-row no-gutters v-if="this.selectedLayer">
        <v-col cols="12">
          <div class="caption text-right ma-2"><a href="#" @click.prevent="enableMapLayer">Enable {{this.selectedLayer}} layer</a></div>
        </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col cols="12" md="6" align-self="center">
          Search options:
          <v-radio-group v-model="searchFullUpstreamArea">
            <v-radio
              label="Entire upstream catchment"
              :value="true"
            ></v-radio>
            <v-radio
              label="Within distance of stream"
              :value="false"
            ></v-radio>
          </v-radio-group>
          <v-text-field
            label="Stream buffer size (m)"
            placeholder="20"
            :rules="[inputRules.number, inputRules.max, inputRules.required]"
            v-model="buffer"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-select
            solo
            :items="layerOptions"
            placeholder="Select a Layer to Analyze"
            v-model="selectedLayer"
          />
        </v-col>
      </v-row>

      <v-row no-gutters>
        <StreamBufferData :loading="loading" :bufferData="streamData" :segmentType="'upstream'" :layerId="selectedLayer" />
      </v-row>
  </v-sheet>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
import ApiService from '../../services/ApiService'
import StreamBufferData from '../analysis/StreamBufferData'
import debounce from 'lodash.debounce'

export default {
  name: 'StreamBufferIntersections',
  components: {
    StreamBufferData
  },
  props: ['record'],
  data: () => ({
    buffer: 50,
    loadingData: false,
    loadingMapFeatures: false,
    panelOpen: [],
    searchFullUpstreamArea: true,
    streamNetworkMapFeature: null,
    streamData: null,
    selectedLayer: '',
    inputRules: {
      required: value => !!value || 'Required',
      number: value => !Number.isNaN(parseFloat(value)) || 'Invalid number',
      max: value => value <= 500 || 'Buffer must be between 0 and 500 m'
    },
    layerOptions: [
      { value: 'groundwater_wells', text: 'Groundwater Wells' },
      { value: 'water_rights_licences', text: 'Water Rights Licences' },
      { value: 'water_rights_applications', text: 'Water Rights Applications' },
      { value: 'ecocat_water_related_reports', text: 'Ecocat Reports' },
      { value: 'aquifers', text: 'Aquifers' },
      { value: 'critical_habitat_species_at_risk', text: 'Critical Habitats' },
      { value: 'water_allocation_restrictions', text: 'Allocation Restrictions' },
      { value: 'hydrometric_stream_flow', text: 'Stream Stations' }
    ]
  }),
  methods: {
    updateStreamBuffers () {
      this.fetchStreamBufferInformation()
    },
    resetGeoJSONLayers () {
      if (this.streamNetworkMapFeature) {
        this.map.removeLayer(this.streamNetworkMapFeature)
        this.map.removeSource(this.streamNetworkMapFeature)
        this.streamNetworkMapFeature = null
      }
    },
    enableMapLayer () {
      this.$store.dispatch('map/addMapLayer', this.selectedLayer)
    },
    updateStreams: debounce(function () {
      this.drawStreamNetwork()
      this.updateStreamBuffers()
    }, 250),
    drawStreamNetwork () {
      if (!this.record || this.buffer < 0) {
        return
      }

      this.resetGeoJSONLayers()

      this.loadingMapFeatures = true

      const linearFeatID = this.record.properties['LINEAR_FEATURE_ID']
      const fwaCode = this.record.properties['FWA_WATERSHED_CODE']

      ApiService.query(
        '/api/v1/stream/features',
        {
          code: fwaCode,
          linear_feature_id: linearFeatID,
          buffer: this.buffer,
          full_upstream_area: this.searchFullUpstreamArea }
      ).then((r) => {
        const data = r.data

        this.streamNetworkMapFeature = 'selectedStreamNetwork'

        this.map.addLayer({
          id: 'selectedStreamNetwork',
          type: 'fill',
          source: {
            type: 'geojson',
            data: data
          },
          layout: {
            visibility: 'visible'
          },
          paint: {
            'fill-color': '#0d47a1',
            'fill-outline-color': '#002171',
            'fill-opacity': 0.3
          }
        }, 'water_rights_licences')
        this.loadingMapFeatures = false
      }).catch(() => {
        this.loadingMapFeatures = false
      })
    },
    fetchStreamBufferInformation () {
      if (this.buffer < 0 || !this.selectedLayer) {
        return
      }
      this.loadingData = true

      this.resetStreamData()

      const fwaCode = this.record.properties['FWA_WATERSHED_CODE']
      const linearFeatID = this.record.properties['LINEAR_FEATURE_ID']

      const params = {
        buffer: parseFloat(this.buffer),
        code: fwaCode,
        linear_feature_id: linearFeatID,
        layer: this.selectedLayer,
        full_upstream_area: this.searchFullUpstreamArea
      }
      ApiService.query('/api/v1/stream/features', params)
        .then((response) => {
          let data = response.data
          this.streamData = data
          this.loadingData = false
        })
        .catch((error) => {
          console.error(error)
          this.loadingData = false
        })
    },
    resetStreamData () {
      this.streamData = null
    },
    ...mapMutations('map', ['setMode'])
  },
  computed: {
    loading () {
      return this.loadingData || this.loadingMapFeatures
    },
    streamName () {
      let gnis = this.record.properties.GNIS_NAME
      return gnis !== 'None' ? gnis : this.record.properties.FEATURE_CODE
    },
    // resultCounts () {
    //   let counts = {}
    //   // loop through the results, and count the number in each layer
    //   for (const key of Object.keys(this.layerOptions)) {
    //     counts[key] = this.results.filter(x => x.display_data_name === key).length
    //   }
    //   return counts
    // },
    ...mapGetters('map', ['isMapReady', 'map'])
  },
  watch: {
    // panelOpen () {
    //   if (this.panelOpen.length > 0) {
    //     this.$store.commit('setStreamAnalysisPanel', true)
    //     this.$store.commit('setStreamBufferData', this.buffer)
    //   } else {
    //     this.$store.commit('setStreamAnalysisPanel', false)
    //     this.$store.commit('resetStreamBufferData')
    //   }
    // },
    isMapReady (value) {
      if (value) {
        this.updateStreamBuffers()
      }
    },
    buffer (value) {
      if (this.buffer >= 0 && this.buffer < this.inputRules.max) {
        this.updateStreams()
      }
    },
    searchFullUpstreamArea () {
      this.updateStreams()
    },
    selectedLayer () {
      this.updateStreamBuffers()
    },
    record () {
      global.config.debug && console.log('[wally] record changed')
      this.drawStreamNetwork()
      this.updateStreamBuffers()
    }
  },
  mounted () {
    if (this.isMapReady) {
      this.drawStreamNetwork()
      this.updateStreamBuffers()
    }
  },
  beforeDestroy () {
    this.setMode({ type: 'interactive', name: 'upstream_downstream' })
    this.resetGeoJSONLayers()
  }
}
</script>

<style>

</style>
