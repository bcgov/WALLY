<template>
  <BarChart :chart-data="chartData" :key="chartKey" class="chart"></BarChart>
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
    chartKey: Number
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
    this.chartData.visible = true
  }
}
</script>
