<template>
  <LegendGroup :legendItems="legendItems()" :groupName="'Water Rights Licences'" />
</template>

<script>
import LegendGroup from '../LegendGroup'

export default {
  name: 'WaterRightsLicencesLegendItem',
  components: { LegendGroup },
  props: {
    item: {}
  },
  methods: {
    legendItems () {
      const childItems = []
      for (let i = 2; i < this.item.color.length - 1; i += 2) {
        global.config.debug && console.log('[wally]', this.item.color[i].constructor)
        if (this.item.color[i].constructor === Array) {
          const text = this.labelLookup(this.item.color[i].join(', '))
          const color = this.item.color[i + 1]
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
        case 'POD':
          return 'Surface Water'
        case 'PG, PWD':
          return 'Groundwater'
        default:
          return code
      }
    }
  }
}
</script>

<style>
</style>
