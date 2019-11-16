<template>
      <v-expansion-panels class="mt-5" multiple>

        <!-- Single point analysis options -->
        <template v-if="record.geometry.type === 'Point'">
          <v-expansion-panel>
            <v-expansion-panel-header class="grey--text text--darken-4 subtitle-1">Find wells near this point</v-expansion-panel-header>
            <v-expansion-panel-content>
              <WellsNearby :record="record"></WellsNearby>
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-header class="grey--text text--darken-4 subtitle-1">Find licences near this point</v-expansion-panel-header>
            <v-expansion-panel-content>
              <WaterRightsLicencesNearby :record="record"></WaterRightsLicencesNearby>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </template>

        <!-- General (does not depend on geometry type) analysis  -->
        <template>
          <v-expansion-panel>
            <v-expansion-panel-header class="grey--text text--darken-4 subtitle-1">First Nations communities, treaty areas, lands</v-expansion-panel-header>
            <v-expansion-panel-content>
              <FirstNationsContactsNearby :record="record"></FirstNationsContactsNearby>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </template>
    </v-expansion-panels>
</template>

<script>
import WellsNearby from '../analysis/WellsNearby.vue'
import WaterRightsLicencesNearby from '../analysis/WaterRightsLicencesNearby'
import FirstNationsContactsNearby from '../analysis/FirstNationsContactsNearby'

export default {
  name: 'FeatureAnalysis',
  components: {
    WellsNearby,
    WaterRightsLicencesNearby,
    FirstNationsContactsNearby
  },
  props: ['record'],
  data: () => ({
  })
}
</script>

<style>

</style>
