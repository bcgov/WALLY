<template>
  <v-sheet class="pt-5">
    <div class="headline">Line</div>
    <v-expansion-panels class="mt-5" multiple v-model="panelOpen">
      <v-expansion-panel>
        <v-expansion-panel-header class="grey--text text--darken-4 subtitle-1">Cross section plot</v-expansion-panel-header>
        <v-expansion-panel-content>
          <WellsCrossSection :record="record" :coordinates="this.record.geometry.coordinates" :panelOpen="open"></WellsCrossSection>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-sheet>
</template>

<script>
import WellsCrossSection from '../analysis/cross_section/WellsCrossSection'
export default {
  name: 'FeatureUserDefinedLine',
  components: {
    WellsCrossSection
  },
  props: ['record'],
  data: () => ({
    radius: 1000,
    panelOpen: []
  }),
  computed: {
    open () {
      return this.panelOpen.length > 0
    }
  }
}
</script>

<style>

</style>
