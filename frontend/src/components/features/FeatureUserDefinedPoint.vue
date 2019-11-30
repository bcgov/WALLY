<template>
  <v-sheet class="pt-5">
    <v-toolbar flat>
      <v-banner color="indigo"
                icon="mdi-map-marker"
                icon-color="white"
                width="100%"
      >
        <v-toolbar-title>
          Point Coordinates
        </v-toolbar-title>
        {{coordinates}}
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
import WaterRightsLicencesNearby from '../analysis/WaterRightsLicencesNearby'

export default {
  name: 'FeatureUserDefined',
  components: {
    WellsNearby,
    WaterRightsLicencesNearby
  },
  props: ['record'],
  data: () => ({
    radius: 1000
  }),
  computed: {
    coordinates () {
      return this.record.geometry.coordinates.map((x) => {
        return x.toFixed(5)
      }).join(', ')
    }
  }
}
</script>

<style>

</style>
