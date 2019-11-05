<template>
  <Plotly :data="data" :layout="layout" :display-mode-bar="false" :key="4" class="chart"></Plotly>
</template>
<script>
import { Plotly } from 'vue-plotly'

export default {
  name: 'Chart',
  components: {
    Plotly
  },
  props: {
    data: Array,
    layout: {
      title: String
    }
  }
}
</script>
