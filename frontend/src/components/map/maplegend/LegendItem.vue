<template>
  <div>
    <v-icon v-if="!item.image" :color="color()" :size="size()" v-bind:style="{webkitTextStrokeWidth: 2, webkitTextStrokeColor: 'black'}">
      {{iconName()}}
    </v-icon>
    <img v-if="item.image" class="" width="20" :src="require(`../../../assets/images/legend/` + item.image + '.png')"/>
    <span class="layerName">{{item.name}}</span>
  </div>
</template>

<script>
export default {
  name: 'LegendIcon',
  props: {
    item: {}
  },
  methods: {
    iconName () {
      switch (this.item.type) {
        case 'line':
          return 'remove'
        case 'fill': // polygon triangle shape
          return 'signal_cellular_4_bar'
        default: // circle
          return 'lens'
      }
    },
    color () {
      var colorType = typeof this.item.color
      if (colorType === 'string') {
        return this.item.color
      } else if (colorType === 'object') {
        if(this.item.color[0] === 'match') {
          console.log(this.item.color)
        } else if (paint.color[0] === 'interpolate') {
          return this.item.color[6]
        }
      }
    },
    size () {
      if (this.item.type === 'line' || this.item.type === 'fill') {
        return 18
      } else {
        return 12
      }
    }
  }
}
</script>

<style>
</style>
