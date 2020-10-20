<template>
  <LegendGroup
    :legendItems="legendItems()"
    :groupName="'Water Licensed Works - Lines'"
  />
</template>

<script>
import LegendGroup from '../LegendGroup'

export default {
  name: 'WaterLicensedWorksLegendItem',
  components: { LegendGroup },
  props: {
    item: {}
  },
  data () {
    return {
      images: [
        'Conduit - Water',
        'Ditch',
        'Flume',
        'Pipeline - Water',
        'Channel-Release',
        'Spillway',
        'Tailrace',
        'Line (Transmission) - Electrical'
      ]
    }
  },
  methods: {
    legendItems () {
      // This is a unique layer because it uses both
      // the line type and images
      // the type is set to line, but if an image exists
      // then that will be rendered by the LegendItem component
      const childItems = []
      global.config.debug && console.log(['wally'], this.item)
      for (let i = 2; i < this.item.color.length - 1; i += 2) {
        global.config.debug &&
          console.log('[wally]', this.item.color[i].constructor)
        if (this.item.color[i].constructor === Array) {
          const text = this.labelLookup(this.item.color[i].join(', '))
          const image = this.lineImage(text)
          const color = this.item.color[i + 1]
          childItems.push({
            text,
            type: 'line',
            color,
            outlineColor: this.item.outlineColor,
            image
          })
        }
      }
      // add svg images to legend
      this.images.forEach((img) => {
        childItems.push({
          text: img,
          image: this.lineImage(img)
        })
      })
      return childItems
    },
    labelLookup (code) {
      switch (code) {
        case 'DB25150000':
          return 'Accessway'
        case 'DB00100000':
          return 'Access Road'
        case 'EA06100200':
          return 'Conduit - Water'
        case 'GA08450000':
          return 'Dam'
        case 'GE09400000':
          return 'Dike/Levee/Berm'
        case 'GA08800000':
          return 'Ditch'
        case 'GB09150000':
          return 'Dugout'
        case 'GA11500000':
          return 'Flume'
        case 'GA21050000':
          return 'Penstock'
        case 'EA21400610':
          return 'Pipeline - Water'
        case 'GB22100000':
          return 'Pond'
        case 'GA05200200':
          return 'Channel-Rearing'
        case 'GB22100210':
          return 'Pond-Rearing'
        case 'GA05200210':
          return 'Channel-Release'
        case 'GB24300000':
          return 'Reservoir'
        case 'GB24300120':
          return 'Reservoir - Balancing'
        case 'DA25050180':
          return 'Road (Paved Divided)'
        case 'DA25100190':
          return 'Road (Paved Undivided)'
        case 'PI11500000':
          return 'Spawning Channel'
        case 'GA28550000':
          return 'Spillway'
        case 'EA16400110':
          return 'Line (Transmission) - Electrical'
        case 'GA30350000':
          return 'Tailrace'
        case 'DB25150000, DB00100000, DA25100190, DA25050180, GB24300120':
          return 'Accessway, Access Road, Road (Paved Undivided), Road (Paved Divided), Reservoir - Balancing'
        case 'GA21050000, GB22100000, GA05200200, GB22100210':
          return 'Penstock, Pond, Channel-Rearing, Pond-Rearing'
        default:
          return code
      }
    },
    lineImage (name) {
      switch (name) {
        case 'Conduit - Water':
          return 'conduit'
        case 'Ditch':
          return 'ditch'
        case 'Flume':
          return 'flume'
        case 'Pipeline - Water':
          return 'pipeline'
        case 'Channel-Release':
          return 'releasechannel'
        case 'Spillway':
          return 'spillway'
        case 'Tailrace':
          return 'tailrace'
        case 'Line (Transmission) - Electrical':
          return 'transmission'
        default:
          return null
      }
    }
  }
}
</script>

<style>
</style>
