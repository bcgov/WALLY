<template>
  <BarChart v-if="data.type === 'bar'" class="chart" :chart-data="chartData" :key="chartKey"></BarChart>
</template>

<script>
import BarChart from '../chart/BarChart'
export default {
  name: 'ChartAPI',
  components: { BarChart },
  props: {
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

    this.chartData.labels = this.data.data_labels
    this.chartData.datasets = this.data.datasets

    // add to datasets
  }
}
</script>
