<template>
  <div>
    <h1>{{chartTitle}}</h1>
    <BarChart :chart-data="chartData" :key="chartKey" class="chart"></BarChart>
  </div>
</template>

<script>
import BarChart from '../chart/BarChart'
import { chartColors } from '../../constants/colors'

export default {
  name: 'ChartWMS',
  components: { BarChart },
  props: {
    features: Array,
    data: Object,
    chartKey: Number,
    chartTitle: String
  },
  data () {
    return {
      chartData: {
        labels: [],
        datasets: [{
          label: 'Bar chart',
          data: [],
          backgroundColor: chartColors.background,
          borderColor: chartColors.border,
          borderWidth: 1
        }],
        visible: true
      }
    }
  },
  mounted () {
    // Reset
    this.chartData = {
      labels: [],
      datasets: [{
        label: 'Bar chart',
        data: [],
        backgroundColor: chartColors.background,
        borderColor: chartColors.border,
        borderWidth: 1
      }],
      visible: true
    }
    this.chartData = this.$attrs.chart.data
    this.chartTitle = this.$attrs.title
    this.chartData.visible = true
  }
}
</script>
