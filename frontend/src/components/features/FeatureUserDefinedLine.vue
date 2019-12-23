<template>
  <v-sheet class="pt-5">
    <div class="headline">Line</div>
    <dl>
      <dt>Coordinates:</dt>
      <dl></dl>
    </dl>
    <v-expansion-panels class="mt-5" multiple>
      <v-expansion-panel>
        <v-expansion-panel-header class="grey--text text--darken-4 subtitle-1">Wells along line</v-expansion-panel-header>
        <v-expansion-panel-content>
          <WellsCrossSection :record="record" :coordinates="this.record.geometry.coordinates"></WellsCrossSection>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-sheet>
</template>

<script>
import WellsCrossSection from '../analysis/WellsCrossSection'
export default {
  name: 'FeatureUserDefinedLine',
  components: {
    WellsCrossSection
  },
  props: ['record'],
  data: () => ({
    radius: 1000
  }),
  computed: {
  }
}
</script>

<style>

</style>
