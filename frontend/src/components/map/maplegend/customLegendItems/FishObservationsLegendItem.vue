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
      if (this.layer.display_data_name === 'fish_observations') {
        return {
          text: this.layer.display_name,
          image: 'fish-icon-orange'
        }
      }
      if (this.layer.display_data_name === 'fish_observations_summaries') {
        return {
          text: this.layer.display_name,
          image: 'fish-icon-red'
        }
      }
    }
  }
}
</script>

<style>
</style>
