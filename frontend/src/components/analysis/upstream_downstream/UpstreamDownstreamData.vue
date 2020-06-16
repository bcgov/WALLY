<template>
    <v-card class="my-2 flex">
        <div class="ml-4 mt-4 title">
            {{title}}
        </div>
        <v-card-text>
          Upstream
          <v-data-table
            :loading="loading"
            :items="upstreamData"
            :headers="headers"
            :items-per-page="5"
          />
        </v-card-text>
        <v-card-text>
          Downstream
          <v-data-table
            :loading="loading"
            :items="downstreamData"
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
    upstreamData () {
      return this.bufferData && this.bufferData.upstream
        ? this.bufferData.upstream.features.map((x) => {
          return x.properties
        }) : []
    },
    downstreamData () {
      return this.bufferData && this.bufferData.downstream
        ? this.bufferData.downstream.features.map((x) => {
          return x.properties
        }) : []
    }
  }
}
</script>

<style>
</style>
