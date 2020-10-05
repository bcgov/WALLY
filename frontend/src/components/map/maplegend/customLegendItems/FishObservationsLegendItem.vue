<template>
  <LegendGroup :legendItems="legendItems()" :groupName="'Fish Observations'" />
</template>

<script>
import LegendGroup from '../LegendGroup'

export default {
  name: 'FishObservationsLegendItem',
  components: { LegendGroup },
  props: {
    item: {}
  },
  methods: {
    legendItems () {
      return [
        {
          text: 'Observation Point',
          image: 'fish-icon-orange'
        },
        {
          text: 'Summary Point',
          image: 'fish-icon-red'
        }
      ]
    }
  }
}
</script>

<style>
</style>
