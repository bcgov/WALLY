<template>
    <v-card class="my-2 flex">
        <div class="ml-4 mt-4 title">
            {{title}}
        </div>
        <v-card-text>
          <v-data-table
            :loading="loading"
            :items="parsedData"
            :headers="headers"
            :items-per-page="5"
          />
        </v-card-text>
    </v-card>
</template>

<script>
import { streamDataHeaders } from '../../../utils/streamDataHeaders'

export default {
  name: 'UpstreamDownstreamData',
  props: [
    'loading',
    'bufferData',
    'segmentType',
    'layerId'
  ],
  data: () => ({
    titleLookup: {
      selectedStream: 'Selected stream network features'
    }
  }),
  computed: {
    title () {
      return this.titleLookup[this.segmentType]
    },
    headers () {
      return streamDataHeaders[this.layerId]
    },
    parsedData () {
      if (!this.bufferData || !this.bufferData.features.length) {
        return []
      }
      return this.bufferData.features.map((x) => {
        return x.properties
      })
    }
  }
}
</script>

<style>
</style>
