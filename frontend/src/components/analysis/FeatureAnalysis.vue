<template>
      <v-expansion-panels class="mt-5" multiple>
        <!-- Single point analysis options -->
        <template v-if="record && record.geometry && record.geometry.type === 'Point'">
          <v-card>
            <v-card-title>
              Near this point
            </v-card-title>
            <v-card-text>
              Choose one of the options below to do a query or analysis on what's near this point of interest
            </v-card-text>
            <v-card-actions>
              <v-btn
                block
                text
                color="deep-purple accent-4"
                class="analysisButton"
                :to="{ path: 'wells-nearby', query: { coordinates: record.geometry.coordinates }}"
              >
               Find Groundwater Wells
                <v-icon>mdi-chevron-right</v-icon>
              </v-btn>
            </v-card-actions>
            <v-card-actions>
              <v-btn
                block
                text
                color="deep-purple accent-4"
                class="analysisButton"
                :to="{ path: 'water-rights-licences-nearby', query: { coordinates: record.geometry.coordinates }}"
              >
                Find Water rights licences
                <v-icon>mdi-chevron-right</v-icon>
              </v-btn>
            </v-card-actions>
            <v-card-actions>
              <v-btn
                block
                text
                color="deep-purple accent-4"
                class="analysisButton"
                :to="{ path: 'first-nations-areas-nearby', query: { coordinates: record.geometry.coordinates }}"
              >
                Find First Nations communities, treaty areas, lands
                <v-icon>mdi-chevron-right</v-icon>
              </v-btn>
            </v-card-actions>
            <v-card-actions>
              <v-btn
                block
                text
                color="deep-purple accent-4"
                class="analysisButton"
                :to="{ path: 'apportion-demand', query: { coordinates: record.geometry.coordinates }}"
              >
                Apportion a stream
                <v-icon>mdi-chevron-right</v-icon>
              </v-btn>
            </v-card-actions>
          </v-card>
<!--          <hr/>-->
<!--          <v-expansion-panel>-->
<!--            <v-expansion-panel-header class="grey&#45;&#45;text text&#45;&#45;darken-4 subtitle-1">Find wells near this point</v-expansion-panel-header>-->
<!--            <v-expansion-panel-content>-->
<!--              <WellsNearby :record="record"></WellsNearby>-->
<!--            </v-expansion-panel-content>-->
<!--          </v-expansion-panel>-->
<!--          <v-expansion-panel>-->
<!--            <v-expansion-panel-header class="grey&#45;&#45;text text&#45;&#45;darken-4 subtitle-1">Find licences near this point</v-expansion-panel-header>-->
<!--            <v-expansion-panel-content>-->
<!--              <WaterRightsLicencesNearby :record="record"></WaterRightsLicencesNearby>-->
<!--            </v-expansion-panel-content>-->
<!--          </v-expansion-panel>-->
<!--          <v-expansion-panel>-->
<!--            <v-expansion-panel-header class="grey&#45;&#45;text text&#45;&#45;darken-4 subtitle-1">Stream apportionment near this point</v-expansion-panel-header>-->
<!--            <v-expansion-panel-content>-->
<!--              <StreamApportionment :record="record"></StreamApportionment>-->
<!--            </v-expansion-panel-content>-->
<!--          </v-expansion-panel>-->
<!--          <v-expansion-panel>-->
<!--            <v-expansion-panel-header class="grey&#45;&#45;text text&#45;&#45;darken-4 subtitle-1">First Nations communities, treaty areas, lands</v-expansion-panel-header>-->
<!--            <v-expansion-panel-content>-->
<!--              <FirstNationsAreasNearby :record="record"></FirstNationsAreasNearby>-->
<!--            </v-expansion-panel-content>-->
<!--          </v-expansion-panel>-->
        </template>

        <!-- General (does not depend on geometry type) analysis  -->
        <template>
        </template>
    </v-expansion-panels>
</template>

<script>
import WellsNearby from './wells_nearby/WellsNearby.vue'
import WaterRightsLicencesNearby from './water_rights_licences_nearby/WaterRightsLicencesNearby'
import FirstNationsAreasNearby from '../analysis/FirstNationsAreasNearby'
import StreamApportionment from './stream_apportionment/StreamApportionment.vue'

export default {
  name: 'FeatureAnalysis',
  components: {
    StreamApportionment,
    WellsNearby,
    WaterRightsLicencesNearby,
    FirstNationsAreasNearby
  },
  props: ['record'],
  data: () => ({
  })
}
</script>

<style>
.analysisButton{
  justify-content: left;
}
</style>
