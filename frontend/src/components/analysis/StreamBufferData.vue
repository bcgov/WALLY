<template>
    <v-card class="my-2 flex">
        <div class="ml-4 mt-4 title">
            {{title}}
        </div>
        <v-card-text>
            <v-data-table
                :items="bufferData"
                :headers="headers"
                :items-per-page="5"
            ></v-data-table>
        </v-card-text>
    </v-card>
</template>

<script>
import { streamDataHeaders } from '../../utils/streamDataHeaders'

export default {
  name: 'StreamBufferData',
  props: [
    'bufferData',
    'segmentType',
    'layerId'
  ],
  data: () => ({
      titleLookup: {
          upstream: 'Up Stream Features',
          downstream: 'Down Stream Features',
          selectedstream: 'Selected Stream Segment Features'
      }
  }),
  computed: {
      title() {
          return this.titleLookup[this.segmentType]
      },
      headers() {
          return streamDataHeaders[this.layerId]
      }
  }
}
</script>

<style>
</style>
