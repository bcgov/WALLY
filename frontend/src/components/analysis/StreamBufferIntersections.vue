<template>
  <v-container>
    <v-row no-gutters>
      <v-col cols="12" md="4" align-self="center">
        <h1>{{streams}}</h1>
        <v-data-table
            :loading="loading"
            :items="streams"
        >
            <!-- <template v-slot:item.distance="{ item }">
                <span>{{item.distance.toFixed(1)}}</span>
            </template>
            <template v-slot:item.QUANTITY="{ item }">
                <span v-if="item.QUANTITY" >{{item.QUANTITY.toFixed(3)}} {{item.QUANTITY_UNITS}}</span>
            </template> -->
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>

</template>

<script>
export default {
  name: 'StreamBufferIntersections',
  components: {
  },
  props: ['streamData'],
  data: () => ({
    buffer: 10,
    loading: false,
    layerOptions: {
        groundwater_wells: true,
        water_rights_licences: true,
        water_rights_applications: true,
        hydrometric_stream_flow: true
    },
    // headers: [
    //   { text: 'Distance', value: 'distance' },
    //   { text: 'Application status', value: 'APPLICATION_STATUS' },
    //   { text: 'Application number', value: 'APPLICATION_JOB_NUMBER' },
    //   { text: 'Licence number', value: 'LICENCE_NUMBER' },
    //   { text: 'POD number', value: 'POD_NUMBER' },
    //   { text: 'POD subtype', value: 'POD_SUBTYPE', filterable: true },
    //   { text: 'Purpose use', value: 'PURPOSE_USE' },
    //   { text: 'Quantity', value: 'QUANTITY' }
    // ],
  }),
  methods: {
      fetchBuffer() {
        this.loading = true

      }
  },
  computed: {
    streams() {
        return this.streamData
    },

    activeLayers() {
        let layers = []
        for (const key of Object.keys(this.layerOptions)) {
            if (this.layerOptions[key]) {
                layers.append(key)
            }
        }
        return layers
    }
  }
}
</script>

<style>

</style>
