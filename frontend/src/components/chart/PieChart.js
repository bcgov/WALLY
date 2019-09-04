import { Pie, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
  name: 'PieChart',
  extends: Pie,
  mixins: [reactiveProp],
  props: ['chartData', 'options'],
  mounted () {
    this.renderChart(this.chartData, this.options)
  },
  watch: {
    chartData () {
      this.$data._chart.update()
    }
  }
}
