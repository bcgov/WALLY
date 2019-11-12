<template>
  <v-sheet class="pt-5">
    <div class="headline">Point</div>
    <dl>
      <dt>Coordinates:</dt>
      <dl>{{coordinates}}</dl>
    </dl>
    <v-expansion-panels class="mt-5" multiple>
      <v-expansion-panel>
        <v-expansion-panel-header class="grey--text text--darken-4 subtitle-1">Find wells near this point</v-expansion-panel-header>
        <v-expansion-panel-content>
          <WellsNearby :record="record" :coordinates="this.record.geometry.coordinates"></WellsNearby>
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel>
        <v-expansion-panel-header class="grey--text text--darken-4 subtitle-1">Find licences near this point</v-expansion-panel-header>
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
