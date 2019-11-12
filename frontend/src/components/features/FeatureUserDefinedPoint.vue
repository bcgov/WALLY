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
          <DistanceToWells :record="record" :coordinates="this.record.geometry.coordinates"></DistanceToWells>
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel>
        <v-expansion-panel-header class="grey--text text--darken-4 subtitle-1">Find licences near this point</v-expansion-panel-header>
        <v-expansion-panel-content>
          <DistanceToLicences :record="record" :coordinates="this.record.geometry.coordinates"></DistanceToLicences>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-sheet>
</template>

<script>
import DistanceToWells from '../analysis/WellsNearby'
import DistanceToLicences from '../analysis/WaterRightsLicencesByDistance'

export default {
  name: 'FeatureUserDefined',
  components: {
    DistanceToWells,
    DistanceToLicences
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
