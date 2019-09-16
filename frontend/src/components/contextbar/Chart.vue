<template>
  <div>
    <h2>{{chartTitle}}</h2>
    <BarChart :chart-data="chartData" :key="chartKey" class="chart"></BarChart>
  </div>
</template>

<script>
import { BarChart } from '../chartjs/Charts'
import { blueChartColors } from '../../constants/colors'

export default {
  name: 'Chart',
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
      },
      chartTitle: String
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
