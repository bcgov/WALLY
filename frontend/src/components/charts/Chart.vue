<template>
  <Plotly :data="data" :layout="layout" :key="4" class="chart" :displaylogo="false"></Plotly>
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
