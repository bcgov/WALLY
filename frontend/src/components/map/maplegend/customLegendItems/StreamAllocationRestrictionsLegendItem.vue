<template>
  <LegendGroup :legendItems="legendItems()" :groupName="'Stream Allocation Restrictions'" />
</template>

<script>
import LegendGroup from '../LegendGroup'

export default {
  name: 'StreamAllocationRestrictionsLegendItem',
  components: { LegendGroup },
  props: {
    item: {}
  },
  methods: {
    legendItems () {
      const childItems = []
      for (let i = 1; i < this.item.color.length; i += 2) {
        if (this.item.color[i].constructor === Array) {
          const text = this.labelLookup(this.item.color[i][2].join(', '))
          const color = this.item.color[i + 1]
          childItems.push({
            text,
            type: 'line',
            color,
            outlineColor: this.item.outlineColor
          })
        }
      }
      return childItems
    },
    labelLookup (code) {
      switch (code) {
        case 'OR':
          return 'Office Reserve'
        case 'FR':
          return 'Fully Recorded'
        case 'FR_EXC':
          return 'Fully Recorded Except'
        case 'PWS':
          return 'Possible Water Shortage'
        case 'PWS, RNW':
          return 'Possible Water Shortage, Refused No Water'
        default:
          return code
      }
    }
  }
}
</script>

<style>
</style>
