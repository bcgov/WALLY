<template>
  <div>
    <h4 class="layerName">{{groupName}}</h4>
    <div v-for="(item, i) in legendItems" v-bind:key="`item${i}`">
      <div class="grouped">
        <LegendItem :item="item" />
      </div>
    </div>
  </div>
</template>

<script>
import LegendItem from './LegendItem'

export default {
  name: 'LegendGroup',
  components: { LegendItem },
  props: {
    legendItems: {},
    groupName: String
  },
  methods: {
  }
}
</script>

<style>
</style>
