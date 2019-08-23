<template>
  <BarChart v-if="data.type === 'bar'" :chart-data="chartData" :key="chartKey"></BarChart>
</template>

<script>
import BarChart from '../chart/BarChart'
import * as chartColors from '../../constants/colors'

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
    this.chartData.labels = []
    this.chartData.datasets.forEach( (dataset, i) => {
      this.chartData.datasets[i].data = []
      this.chartData.datasets[i].label = ''
    })

    // Build chart data
    this.features.forEach(item => {
      this.chartData.labels.push(item.properties[this.data.label_key])
      this.data.datasets_key.forEach((datasetKey, i) => {
        this.chartData.datasets[i].label = this.data.datasets_labels[i]
        this.chartData.datasets[i].data.push(item.properties[datasetKey])
      })
      // this.chartData.datasets[0].borderColor.push('rgba(54, 162, 235, 1)')
      // this.chartData.datasets[0].backgroundColor.push('rgba(54, 162, 235, 0.2)')
      // console.log(this.chartData)
    })
  }
}
</script>
