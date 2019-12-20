<template>
  <v-sheet class="pt-5">
    <v-toolbar flat>
      <v-banner color="indigo"
                icon="mdi-map-marker"
                icon-color="white"
                width="100%"
      >
        <v-toolbar-title>
          {{streamName}}
        </v-toolbar-title>
          Selected Stream
      </v-banner>
    </v-toolbar>
    <v-expansion-panels class="mt-5" multiple v-model="panelOpen">
      <v-expansion-panel>
        <v-expansion-panel-header class="grey--text text--darken-4 subtitle-1">Up Stream/Down Stream Features</v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-row no-gutters v-if="this.selectedLayer">
            <v-col cols="12">
              <div class="caption text-right ma-2"><a href="#" @click.prevent="enableMapLayer">Enable {{this.selectedLayer}} layer</a></div>
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-col cols="12" md="3" align-self="center">
              <v-text-field
                label="Stream Buffer Size (m)"
                placeholder="20"
                :rules="[inputRules.number, inputRules.max, inputRules.required]"
                v-model="buffer"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="3" />
            <v-col cols="12" md="6">
              <v-select
                solo
                :items="layerOptions"
                placeholder="Select a Layer to Analyze"
                v-model="selectedLayer"
              ></v-select>
            </v-col>
          </v-row>

          <v-row no-gutters>
            <SteamBufferData :bufferData="upStreamData" :segmentType="'upstream'" :layerId="selectedLayer" />
            <SteamBufferData :bufferData="selectedStreamData" :segmentType="'selectedStream'" :layerId="selectedLayer" />
            <SteamBufferData :bufferData="downStreamData" :segmentType="'downstream'" :layerId="selectedLayer" />
          </v-row>

        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-sheet>
</template>

<script>
import { mapGetters } from 'vuex'
import ApiService from '../../services/ApiService'
import SteamBufferData from '../analysis/StreamBufferData'
import buffer from '@turf/buffer'

export default {
  name: 'StreamBufferIntersections',
  components: {
    SteamBufferData
  },
  props: ['record'],
  data: () => ({
    buffer: 50,
    loading: false,
    panelOpen: [],
    upStreamData: [],
    selectedStreamData: [],
    downStreamData: [],
    selectedLayer: '',
    inputRules: {
      required: value => !!value || 'Required',
      number: value => !Number.isNaN(parseFloat(value)) || 'Invalid number',
      max: value => value <= 500 || 'Buffer must be between 0 and 500 m'
    },
    layerOptions: [
      { value: 'groundwater_wells', text: 'Ground Water Wells' },
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
      this.fetchStreamBufferInformation(this.getUpStreamData, 'upstream')
      this.fetchStreamBufferInformation(this.getDownStreamData, 'downstream')
      this.fetchStreamBufferInformation(this.getSelectedStreamData, 'selectedStream')
    },
    enableMapLayer () {
      this.$store.commit('addMapLayer', this.selectedLayer)
    },
    fetchStreamBufferInformation (streams, type) {
      if (buffer <= 0 || !this.selectedLayer) {
        return
      }

      let lineStrings = streams.features.map((stream) => {
        if (stream.geometry.type === 'LineString') {
          return stream.geometry
        }
      })
      if (lineStrings.length <= 0) {
        return
      }
      const params = {
        buffer: parseFloat(this.buffer),
        geometry: JSON.stringify(lineStrings),
        layer: this.selectedLayer
      }
      this.loading = true
      ApiService.post('/api/v1/stream/features', params)
        .then((response) => {
          let data = response.data
          if (type === 'upstream') {
            this.upStreamData = data
          } else if (type === 'downstream') {
            this.downStreamData = data
          } else if (type === 'selectedStream') {
            this.selectedStreamData = data
          }
          this.loading = false
        })
        .catch((error) => {
          console.log(error)
        })
    }
  },
  computed: {
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
    ...mapGetters([
      'getUpStreamData',
      'getDownStreamData',
      'getSelectedStreamData'
    ])
  },
  watch: {
    panelOpen () {
      if (this.panelOpen.length > 0) {
        this.$store.commit('setStreamAnalysisPanel', true)
        this.$store.commit('setStreamBufferData', this.buffer)
      } else {
        this.$store.commit('setStreamAnalysisPanel', false)
        this.$store.commit('resetStreamBufferData')
      }
    },
    getUpStreamData () {
      if (this.panelOpen.length > 0) {
        this.fetchStreamBufferInformation(this.getUpStreamData, 'upstream')
        this.$store.commit('setUpStreamBufferData', this.buffer)
      }
    },
    getDownStreamData () {
      if (this.panelOpen.length > 0) {
        this.fetchStreamBufferInformation(this.getDownStreamData, 'downstream')
        this.$store.commit('setDownStreamBufferData', this.buffer)
      }
    },
    getSelectedStreamData () {
      if (this.panelOpen.length > 0) {
        this.fetchStreamBufferInformation(this.getSelectedStreamData, 'selectedStream')
        this.$store.commit('setSelectedStreamBufferData', this.buffer)
      }
    },
    buffer (value) {
      if (this.buffer > 0 && this.buffer < this.inputRules.max) {
        this.updateStreamBuffers()
        this.$store.commit('setStreamBufferData', value)
      }
    },
    selectedLayer () {
      this.updateStreamBuffers()
    }
  }
}
</script>

<style>

</style>
