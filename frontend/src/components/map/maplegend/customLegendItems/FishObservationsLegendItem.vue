<template>
  <LegendItem :item="legendItem()" />
</template>

<script>
import LegendItem from '../LegendItem'

export default {
  name: 'FishObservationsLegendItem',
  components: { LegendItem },
  props: ['layer'],
  methods: {
    legendItem () {
      if (this.layer === 'fish_observations') {
        return {
          text: 'Known BC Fish Observation Point',
          image: 'fish-icon-orange'
        }
      }
      if (this.layer === 'fish_observations_summaries') {
        return {
          text: 'Known BC Fish Observations Summary',
          image: 'fish-icon-red'
        }
      }
    }
  }
}
</script>

<style>
</style>
