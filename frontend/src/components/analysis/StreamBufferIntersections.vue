<template>
  <v-container>
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
          :items="layerOptions"
          placeholder="Select a Layer to Analyze"
          solo
        ></v-select>
      </v-col>

      
      <v-card class="my-2">
        <v-card-title>
        Upstream Segments
        </v-card-title>
        <v-card-text>
        <v-data-table
          :loading="loading"
          v-if="results"
          :items="results"
          :headers="headers"
        ></v-data-table>
        </v-card-text>
      </v-card>

      <v-card class="my-2">
        <v-card-title>
        Selected Stream Segment
      </v-card-title>
        <v-card-text>
        <v-data-table
          :loading="loading"
          v-if="results"
          :items="results"
          :headers="headers"
        ></v-data-table>
        </v-card-text>
      </v-card>

      <v-card class="my-2">
        <v-card-title>
        Downstream Segments
      </v-card-title>
        <v-card-text>
        <v-data-table
          :loading="loading"
          v-if="results"
          :items="results"
          :headers="headers"
        ></v-data-table>
        </v-card-text>
      </v-card>

    </v-row>
  </v-container>

</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import ApiService from '../../services/ApiService'
import EventBus from '../../services/EventBus'
import buffer from '@turf/buffer'
import union from '@turf/union'
import qs from 'querystring'

export default {
  name: 'StreamBufferIntersections',
  components: {
  },
  props: ['streamData'],
  data: () => ({
    buffer: 10,
    inputRules: {
      required: value => !!value || 'Required',
      number: value => !Number.isNaN(parseFloat(value)) || 'Invalid number',
      max: value => value <= 100 || 'Buffer must be between 0 and 100 m'
    },
    loading: false,
    // layerOptions: {
    //     groundwater_wells: true,
    //     water_rights_licences: false,
    //     water_rights_applications: false,
    //     hydrometric_stream_flow: false
    // },
    layerOptions: [
      'Ground Water Wells',
      'Water Rights Licences',
      'Water Rights Applications',
      'Stream Stations'
    ],
    results: [],
    headers: [
      { text: 'Distance', value: 'distance' },
      { text: 'Application status', value: 'APPLICATION_STATUS' },
      { text: 'Application number', value: 'APPLICATION_JOB_NUMBER' },
      { text: 'Licence number', value: 'LICENCE_NUMBER' },
      { text: 'POD number', value: 'POD_NUMBER' },
      { text: 'POD subtype', value: 'POD_SUBTYPE', filterable: true },
      { text: 'Purpose use', value: 'PURPOSE_USE' },
      { text: 'Quantity', value: 'QUANTITY' }
    ],
  }),
  methods: {
    fetchStreamBufferIntersections() {
      this.loading = true

      // var layers = this.activeLayers.map((layer) => {
      //     return 'layers=' + layer + '&'
      // })
      // let bufferPolygons = this.streams.features.map((stream) => {
      //   return buffer(stream.geometry, this.buffer, {units: 'meters'})
      // })
      // let mergedPolygon = union(...bufferPolygons)

      let lineStrings = this.streams.features.map((stream) => {
        return stream
      })
      let mergedLineStrings = union(...lineStrings)

      const params = {
        buffer: parseFloat(this.buffer),
        geometry: JSON.stringify(mergedLineStrings.geometry)
      }

      ApiService.query(`/api/v1/analysis/licences/buffer?${qs.stringify(params)}`)
        .then((response) => {
          
          // let displayData = response.data.display_data
          // if (!displayData.some(layer => {
          //   return layer.geojson && layer.geojson.features.length
          // })) {
          //   EventBus.$emit('info', 'No features were found in your search area.')
          //   return
          // }
          // displayData.forEach(layer => {
          //   this.results[layer] = layer.geojson.features
          // })
          console.log(response)
          this.results = response.data
          this.loading = false
        })
        .catch((error) => {
          console.log(error)
        })
    }   

  },
  computed: {
    streams() {
        return this.streamData
    },
    // activeLayers() {
    //     let layers = []
    //     for (const key of Object.keys(this.layerOptions)) {
    //         if (this.layerOptions[key]) {
    //             layers.push(key)
    //         }
    //     }
    //     return layers
    // },
    resultCounts () {
      let counts = {}
      // loop through the results, and count the number in each layer
      for (const key of Object.keys(this.layerOptions)) {
        counts[key] = this.results.filter(x => x.display_data_name === key).length
      }
      return counts
    },
    // ...mapGetters(['getSelectedStreamData'])
  },
  watch: {
    streamData: {
      handler () {
        this.fetchStreamBufferIntersections()
      }
    },
    // getSelectedStreamData(value) {
    //   this.fetchStreamBufferIntersections()
    // },
    buffer (value) {
      this.fetchStreamBufferIntersections()
    }
  },
}
</script>

<style>

</style>
