<template>
  <v-sheet class="pa-5">
    <v-row>
      <v-col cols="12" md="12">
        <v-expansion-panels>
          <v-expansion-panel>
            <v-expansion-panel-header>
              Instructions
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-card flat>
                <v-card-text>
                  <UpstreamDownstreamInstructions></UpstreamDownstreamInstructions>
                </v-card-text>
              </v-card>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols=12 md=6>
        <div class="title my-3">
          Selected Stream: {{streamName}}
        </div>
      </v-col>
      <v-col class="text-right">
        <v-btn class="ml-3" @click="selectPoint" color="primary" outlined :disabled="buttonClicked">Select a point</v-btn>
      </v-col>
    </v-row>

      <v-row no-gutters v-if="this.selectedLayer">
        <v-col cols="12">
          <div class="caption text-right ma-2"><a href="#" @click.prevent="enableMapLayer">Enable {{selectedLayerName}} layer</a></div>
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
        <UpstreamDownstreamData :loading="loading" :bufferData="streamData" :segmentType="'upstream'" :layerId="selectedLayer" />
      </v-row>
  </v-sheet>
</template>

<script>
import { mapGetters, mapMutations, mapActions } from 'vuex'
import ApiService from '../../../services/ApiService'
import UpstreamDownstreamData from './UpstreamDownstreamData'
import UpstreamDownstreamInstructions from './UpstreamDownstreamInstructions'
import debounce from 'lodash.debounce'

export default {
  name: 'StreamBufferIntersections',
  components: {
    UpstreamDownstreamData,
    UpstreamDownstreamInstructions
  },
  props: ['record', 'point'],
  data: () => ({
    buffer: 50,
    loadingData: false,
    loadingMapFeatures: false,
    buttonClicked: false,
    panelOpen: [],
    searchFullUpstreamArea: true,
    upstreamNetworkMapFeature: null,
    downstreamNetworkMapFeature: null,
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
      { value: 'ecocat_water_related_reports', text: 'EcoCat Reports' },
      { value: 'aquifers', text: 'Aquifers' },
      { value: 'critical_habitat_species_at_risk', text: 'Critical Habitats' },
      { value: 'water_allocation_restrictions', text: 'Allocation Restrictions' },
      { value: 'hydrometric_stream_flow', text: 'Stream Stations' }
    ]
  }),
  methods: {
    selectPoint () {
      this.setDrawMode('draw_point')
      this.buttonClicked = true
    },
    updateStreamBuffers () {
      this.fetchStreamBufferInformation()
    },
    resetGeoJSONLayers () {
      if (this.upstreamNetworkMapFeature) {
        this.map.removeLayer(this.upstreamNetworkMapFeature)
        this.map.removeSource(this.upstreamNetworkMapFeature)
        this.upstreamNetworkMapFeature = null
      }
      if (this.downstreamNetworkMapFeature) {
        this.map.removeLayer(this.downstreamNetworkMapFeature)
        this.map.removeSource(this.downstreamNetworkMapFeature)
        this.downstreamNetworkMapFeature = null
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
          full_upstream_area: this.searchFullUpstreamArea,
          point: this.point
        }
      ).then((r) => {
        const data = r.data
        console.log(data)
        this.upstreamNetworkMapFeature = 'upstreamNetwork'
        this.downstreamNetworkMapFeature = 'downstreamNetwork'

        this.map.addLayer({
          id: this.upstreamNetworkMapFeature,
          type: 'fill',
          source: {
            type: 'geojson',
            data: data.upstream
          },
          layout: {
            visibility: 'visible'
          },
          paint: {
            'fill-color': '#99CC99',
            'fill-outline-color': '#002171',
            'fill-opacity': 0.65
          }
        }, 'water_rights_licences')

        this.map.addLayer({
          id: this.downstreamNetworkMapFeature,
          type: 'fill',
          source: {
            type: 'geojson',
            data: data.downstream
          },
          layout: {
            visibility: 'visible'
          },
          paint: {
            'fill-color': '#0d47a1',
            'fill-outline-color': '#002171',
            'fill-opacity': 0.5
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
    ...mapActions(['exitFeature']),
    ...mapActions('map', ['setDrawMode', 'clearSelections']),
    ...mapMutations('map', ['setMode'])
  },
  computed: {
    selectedLayerName () {
      return this.layerOptions.find(x => {
        return x.value === this.selectedLayer
      }).text
    },
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
    //     this.$store.commit('setUpstreamDownstreamData', this.buffer)
    //   } else {
    //     this.$store.commit('setStreamAnalysisPanel', false)
    //     this.$store.commit('resetUpstreamDownstreamData')
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
    record (value) {
      global.config.debug && console.log('[wally] record changed')
      this.drawStreamNetwork()
      this.updateStreamBuffers()
      if (value && value.geometry) {
        this.buttonClicked = false
      }
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
