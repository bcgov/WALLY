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
        </template>

        <!-- General (does not depend on geometry type) analysis  -->
        <template>
        </template>
    </v-expansion-panels>
</template>

<script>
export default {
  name: 'FeatureAnalysis',
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
