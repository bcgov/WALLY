<template>
  <v-sheet class="pt-5">
    <v-toolbar flat>
      <v-banner color="indigo"
                icon="mdi-map-marker"
                icon-color="white"
                width="100%"
      >
        <v-toolbar-title>
          {{this.record.properties.GNIS_NAME}}
        </v-toolbar-title>
          Selected Stream 
      </v-banner>
    </v-toolbar>
    <v-expansion-panels class="mt-5" multiple>
      <v-expansion-panel>
        <v-expansion-panel-header class="grey--text text--darken-4 subtitle-1">Up/Down Stream Analysis</v-expansion-panel-header>
        <v-expansion-panel-content>
          <StreamBufferIntersections :streamData="getUpStreamData"></StreamBufferIntersections>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-sheet>
</template>

<script>
import StreamBufferIntersections from '../analysis/StreamBufferIntersections'
import { mapGetters } from 'vuex'

export default {
  name: 'FeatureStreamBuffers',
  components: {
    StreamBufferIntersections
  },
  props: ['record'],
  data: () => ({
    buffer: 10
  }),
  computed: {
    ...mapGetters([
      'getSelectedStreamData',
      'getUpStreamData',
      'getDownStreamData'
    ])
  },
}
</script>

<style>
</style>
