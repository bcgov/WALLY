<template>
  <LegendGroup :legendItems="legendItems()" :groupName="'Water Approval Points'" />
</template>

<script>
import LegendGroup from '../LegendGroup'

export default {
  name: 'WaterApprovalPointsLegendItem',
  components: { LegendGroup },
  props: {
    item: {}
  },
  methods: {
    legendItems () {
      var childItems = []
      for (let i = 2; i < this.item.color.length - 1; i += 2) {
        global.config.debug && console.log('[wally]', this.item.color[i].constructor)
        if (this.item.color[i].constructor === Array) {
          var text = this.labelLookup(this.item.color[i].join(', '))
          var color = this.item.color[i + 1]
          childItems.push({
            text,
            type: 'circle',
            color,
            outlineColor: this.item.outlineColor
          })
        }
      }
      return childItems
    },
    labelLookup (code) {
      switch (code) {
        case 'Current':
          return 'Active Approvals'
        case 'Refuse/Abandoned, Cancelled':
          return 'Non-Active Approvals'
        default:
          return code
      }
    }
  }
}
</script>

<style>
</style>
