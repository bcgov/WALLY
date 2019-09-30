<template>
  <div>
    <h2 class="mb-3 text-center">{{chartTitle}}</h2>
    <bar-chart v-if="chartType==='bar'" :chart-data="chartData" :options="chartOptions" :key="chartKey" class="chart" />
    <line-chart v-if="chartType==='line'" :chart-data="chartData" :options="chartOptions" :key="chartKey" class="chart" />
    <doughnut-chart v-if="chartType==='doughnut'" :chart-data="chartData" :options="chartOptions" :key="chartKey" class="chart" />
    <pie-chart v-if="chartType==='pie'" :chart-data="chartData" :options="chartOptions" :key="chartKey" class="chart" />
  </div>
</template>

<script>
import { BarChart, LineChart, DoughnutChart, PieChart } from '../chartjs/Charts'

import { blueChartColors } from '../../constants/colors'
export default {
  name: 'Chart',
  components: { BarChart, LineChart, DoughnutChart, PieChart },
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
      chartTitle: String,
      chartType: String,
      chartOptions: []
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
    this.chartType = this.$attrs.chart.type
    console.log(this.chartType)
    this.chartOptions = this.$attrs.chart.options
    this.chartData.datasets.forEach((dataset, i) => {
      this.chartData.datasets[i].backgroundColor = blueChartColors.background
      this.chartData.datasets[i].borderColor = blueChartColors.borderColor
    })
    this.chartTitle = this.$attrs.title
    this.chartData.visible = true
  }
}
</script>
