<template>
  <Plotly :data="data" :layout="layout" :key="id" class="chart" :display-mode-bar="false" :displaylogo="false" link="true"></Plotly>
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
  },
  data () {
    return {
      id: null
    }
  },
  mounted () {
    this.id = this._uid
  }
}
</script>
