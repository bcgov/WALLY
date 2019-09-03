<template>
  <div>
    <h1>{{chartTitle}}</h1>
    <BarChart :chart-data="chartData" :key="chartKey" class="chart"></BarChart>
  </div>
</template>

<script>
import BarChart from '../chart/BarChart'
import { blueChartColors } from '../../constants/colors'

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
          backgroundColor: blueChartColors.background,
          borderColor: blueChartColors.border,
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
        backgroundColor: blueChartColors.background,
        borderColor: blueChartColors.border,
        borderWidth: 1
      }],
      visible: true
    }
    this.chartData = this.$attrs.chart.data
    this.chartData.datasets.forEach((dataset, i) => {
      this.chartData.datasets[i].backgroundColor = blueChartColors.background
      this.chartData.datasets[i].borderColor = blueChartColors.borderColor
    })
    this.chartTitle = this.$attrs.title
    this.chartData.visible = true
  }
}
</script>
