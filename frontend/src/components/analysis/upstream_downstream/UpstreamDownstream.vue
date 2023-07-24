<template>
  <v-sheet class="pa-5">
    <v-row v-if="loadingData">
      <v-col>
        <v-progress-linear show indeterminate></v-progress-linear>
      </v-col>
    </v-row>
    <v-alert
      v-if="apiError"
      class="my-5 mx-5"
      outlined
      type="warning"
      prominent
      border="left"
    >
      <p>
        {{apiError}}
      </p>
    </v-alert>
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
          Selected Stream: {{cleanStreamName}}
        </div>
      </v-col>
      <v-col class="text-right">
        <SavedAnalysesCreateModal :geometry="pointOfInterest.geometry" featureType="upstream-downstream"/>
        <v-btn class="ml-3 my-2" @click="selectPoint" color="primary" outlined :disabled="buttonClicked">Select a point</v-btn>
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
        <UpstreamDownstreamData :loading="loadingData" :bufferData="streamData" :segmentType="'upstream'" :layerId="selectedLayer" />
      </v-row>
  </v-sheet>
</template>

<script>
import { mapGetters, mapMutations, mapActions } from 'vuex'
import ApiService from '../../../services/ApiService'
import UpstreamDownstreamData from './UpstreamDownstreamData'
import UpstreamDownstreamInstructions from './UpstreamDownstreamInstructions'
import debounce from 'lodash.debounce'
import { findWallyLayer } from '../../../common/utils/mapUtils'
import { SOURCE_DOWNSTREAM_NETWORK, SOURCE_UPSTREAM_NETWORK } from '../../../common/mapbox/sourcesWally'
import SavedAnalysesCreateModal from '../../savedanalyses/SavedAnalysesCreateModal'

export default {
  name: 'StreamBufferIntersections',
  components: {
    UpstreamDownstreamData,
    UpstreamDownstreamInstructions,
    SavedAnalysesCreateModal
  },
  props: ['point'],
  data: () => ({
    buffer: 50,
    loadingData: false,
    apiError: null,
    loadingMapFeatures: false,
    buttonClicked: false,
    panelOpen: [],
    searchFullUpstreamArea: true,
    upstreamNetworkMapFeature: null,
    downstreamNetworkMapFeature: null,
    streamData: null,
    streamName: '',
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
      this.selectPointOfInterest()
      this.buttonClicked = true
    },
    resetGeoJSONLayers () {
      if (this.map.getLayer(SOURCE_UPSTREAM_NETWORK)) {
        this.map.removeLayer(SOURCE_UPSTREAM_NETWORK)
        this.map.removeSource(SOURCE_UPSTREAM_NETWORK)
      }
      if (this.map.getLayer(SOURCE_DOWNSTREAM_NETWORK)) {
        this.map.removeLayer(SOURCE_DOWNSTREAM_NETWORK)
        this.map.removeSource(SOURCE_DOWNSTREAM_NETWORK)
      }
    },
    enableMapLayer () {
      this.$store.dispatch('map/addMapLayer', this.selectedLayer)
    },
    updateStreams: debounce(function () {
      this.drawStreamNetwork()
    }, 250),
    drawStreamNetwork () {
      if (this.buffer < 0) {
        return
      }

      this.$router.push({
        query:
          { ...this.$route.query,
            coordinates: this.pointOfInterest.geometry.coordinates
          }
      })

      this.resetGeoJSONLayers()
      this.resetStreamData()
      this.loadingData = true
      this.apiError = null

      ApiService.query(
        '/api/v1/streams/features',
        {
          layer: this.selectedLayer,
          buffer: this.buffer,
          full_upstream_area: this.searchFullUpstreamArea,
          point: this.point
        }
      ).then((r) => {
        const data = r.data
        // this.upstreamNetworkMapFeature = 'upstreamNetwork'
        // this.downstreamNetworkMapFeature = 'downstreamNetwork'

        this.streamData = data
        this.streamName = data.gnis_name
        this.loadingData = false

        const upstreamNetworkLayer = findWallyLayer(SOURCE_UPSTREAM_NETWORK)
        this.map.addLayer(upstreamNetworkLayer(data), 'water_rights_licences')

        const downstreamNetworkLayer = findWallyLayer(SOURCE_DOWNSTREAM_NETWORK)
        this.map.addLayer(downstreamNetworkLayer(data), 'water_rights_licences')
      }).catch((e) => {
        this.loadingData = false
        if (!e.response) {
          this.apiError = 'The selected stream segement was too large to process, please choose a smaller segment. (' + e.message + ')'
          return
        }
        this.apiError = 'There was an error getting the stream information: ' + e.message
      })
    },
    resetStreamData () {
      this.streamData = null
    },
    ...mapActions(['exitFeature']),
    ...mapActions('map', ['setDrawMode', 'clearSelections', 'selectPointOfInterest']),
    ...mapMutations('map', ['setMode'])
  },
  computed: {
    selectedLayerName () {
      return this.layerOptions.find(x => {
        return x.value === this.selectedLayer
      }).text
    },
    cleanStreamName () {
      return this.streamName != null ? this.streamName : ''
    },
    ...mapGetters(['pointOfInterest']),
    ...mapGetters('map', ['isMapReady', 'map'])
  },
  watch: {
    isMapReady (value) {
      if (value) {
        this.drawStreamNetwork()
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
      this.drawStreamNetwork()
    },
    pointOfInterest (value) {
      console.log('Point of Intereset seen')
      global.config.debug && console.log('[wally] record changed')
      this.drawStreamNetwork()
      if (value && value.geometry) {
        this.buttonClicked = false
      }
    }
  },
  mounted () {
    if (this.isMapReady) {
      this.drawStreamNetwork()
    }
  },
  beforeDestroy () {
    this.setMode({ type: 'interactive', name: 'upstream_downstream' })
    this.resetGeoJSONLayers()
    this.resetStreamData()
  }
}
</script>

<style>

</style>
