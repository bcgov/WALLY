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
            <SteamBufferData :bufferData="upstreamData" :segmentType="'upstream'" :layerId="selectedLayer" />
            <SteamBufferData :bufferData="selectedStreamData" :segmentType="'selectedstream'" :layerId="selectedLayer" />
            <SteamBufferData :bufferData="downStreamData" :segmentType="'downstream'" :layerId="selectedLayer" />
          </v-row>

        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-sheet>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import ApiService from '../../services/ApiService'
import EventBus from '../../services/EventBus'
import SteamBufferData from '../analysis/StreamBufferData'
import buffer from '@turf/buffer'
import union from '@turf/union'
import qs from 'querystring'

export default {
  name: 'StreamBufferIntersections',
  components: {
    SteamBufferData
  },
  props: ['record'],
  data: () => ({
    buffer: 50,
    loading: false,
    panelOpen: false,
    upstreamData: [],
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
    updateStreamBuffers() {
      this.fetchStreamBuffers(this.getUpStreamData, 'upstream')
      this.fetchStreamBuffers(this.getDownStreamData, 'downstream')
      this.fetchStreamBuffers(this.getSelectedStreamData, 'selectedstream')
    },
    enableMapLayer () {
      this.$store.commit('addMapLayer', this.selectedLayer)
    },
    fetchStreamBuffers(streams, type) {
      let lineStrings = streams.features.map((stream) => {
        return stream.geometry
      })
      if(lineStrings.length <= 0) { 
        return 
      }
      // let mergedLineStrings = union(...lineStrings)

      const params = {
        buffer: parseFloat(this.buffer),
        geometry: JSON.stringify(lineStrings),
        layer: this.selectedLayer
      }
      this.loading = true
      ApiService.query(`/api/v1/analysis/stream/features?${qs.stringify(params)}`)
        .then((response) => {
          let data = response.data
          if (type === 'upstream') {
            this.upstreamData = data
          } else if(type === 'downstream') {
            this.downStreamData = data
          } else if(type === 'selectedstream'){
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
    streamName() {
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
    panelOpen() {
      if(this.panelOpen.length > 0) {
        this.$store.commit('setStreamBufferData', this.buffer)
      } else {
        this.$store.commit('resetStreamBufferData')
      }
    },
    getSelectedStreamData() {
      this.updateStreamBuffers()
      if(this.panelOpen.length > 0) {
        this.$store.commit('setStreamBufferData', this.buffer)
      }
    },
    buffer (value) {
      this.updateStreamBuffers()
      if(this.panelOpen.length >  0) {
        this.$store.commit('setStreamBufferData', value)
      }
    }
  },
}
</script>

<style>

</style>
