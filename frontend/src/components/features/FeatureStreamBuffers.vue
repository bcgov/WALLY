<template>
  <v-sheet class="pt-5">
    <v-toolbar flat>
      <v-banner color="indigo"
                icon="mdi-map-marker"
                icon-color="white"
                width="100%"
      >
        <v-toolbar-title>
          Selected Stream
        </v-toolbar-title>
        {{this.record.properties.GNIS_NAME}}
      </v-banner>
    </v-toolbar>
    <v-expansion-panels class="mt-5" multiple>
      <v-expansion-panel>
        <v-expansion-panel-header class="grey--text text--darken-4 subtitle-1">Find wells near this point</v-expansion-panel-header>
        <v-expansion-panel-content>
          <WellsNearby :record="record" :coordinates="this.record.geometry.coordinates"></WellsNearby>
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel>
        <v-expansion-panel-header class="grey--text text--darken-4 subtitle-1">Find licences and applications near this point</v-expansion-panel-header>
        <v-expansion-panel-content>
          <WaterRightsLicencesNearby :record="record" :coordinates="this.record.geometry.coordinates"></WaterRightsLicencesNearby>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-sheet>
</template>

<script>
import WellsNearby from '../analysis/WellsNearby.vue'
import StreamRelatedPoints from '../analysis/StreamRelatedPoints'

export default {
  name: 'FeatureStreamBuffers',
  components: {
    StreamRelatedPoints
  },
  props: ['record'],
  data: () => ({
    buffer: 10
  }),
  computed: {
    
  }
}
</script>

<style>

</style>
