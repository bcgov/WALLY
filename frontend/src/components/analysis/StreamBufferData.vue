<template>
    <v-card class="my-2">
        <div class="ml-4 mt-4 title">
            {{title}}
        </div>
        <v-card-text>
            <v-data-table
                :items="bufferData"
                :headers="headers"
            ></v-data-table>
        </v-card-text>
    </v-card>
</template>

<script>
import { streamDataHeaders } from '../../utils/streamDataHeaders'

export default {
  name: 'StreamBufferData',
  components: {
  },
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
  methods: {
  },
  computed: {
      title() {
          return this.titleLookup[this.segmentType]
      },
      headers() {
          return streamDataHeaders[this.layerId]
      }
  },
  watch: {
  },
}
</script>

<style>

</style>
