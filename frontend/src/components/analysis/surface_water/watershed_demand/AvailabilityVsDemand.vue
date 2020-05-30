<template>
  <div v-if="demandAvailabilityData">
      <div class="subtitle-1 my-3 font-weight-bold">Availability vs Licensed Quantity</div>
      <div class="my-3"><span class="font-weight-bold">How to read this graph:</span>
        this graph shows available water after allocation from existing surface water licences,
        as determined by subtracting licensed quantities (including any adjusted monthly allocation
        values) from the estimated discharge for each month.
      </div>
      <Plotly v-if="availabilityPlotData && licencePlotData && shortTermLicencePlotData"
              :layout="demandAvailabilityLayout()"
              :data="demandAvailabilityData"
      ></Plotly>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
const Plotly = () => import('vue-plotly').then(module => {
  return module.Plotly
})

export default {
  name: 'AvailabilityVsDemand',
  components: {
    Plotly
  },
  props: [],
  data: () => ({
    months: { 1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31 },
    monthHeaders: [
      { text: 'Jan', value: 'm1' },
      { text: 'Feb', value: 'm2' },
      { text: 'Mar', value: 'm3' },
      { text: 'Apr', value: 'm4' },
      { text: 'May', value: 'm5' },
      { text: 'Jun', value: 'm6' },
      { text: 'Jul', value: 'm7' },
      { text: 'Aug', value: 'm8' },
      { text: 'Sep', value: 'm9' },
      { text: 'Oct', value: 'm10' },
      { text: 'Nov', value: 'm11' },
      { text: 'Dec', value: 'm12' }
    ]
  }),
  computed: {
    ...mapGetters('map', ['map']),
    ...mapGetters('surfaceWater', ['availabilityPlotData', 'licencePlotData', 'shortTermLicencePlotData']),
    demandAvailabilityData () {
      if (!this.availabilityPlotData) {
        return null
      }
      var plotConfig = []
      let mar = this.availabilityPlotData.reduce((a, b) => a + b, 0) / 12

      const availabilityData = {
        type: 'bar',
        name: 'Available Water',
        y: this.availabilityPlotData.map((val, i) => { return val - this.licencePlotData[i] - this.shortTermLicencePlotData[i] }),
        x: this.monthHeaders.map((h) => h.text),
        hovertemplate: '%{y:.2f} m³'
      }

      const mad30 = {
        type: 'line',
        mode: 'lines',
        hoverinfo: 'skip',
        name: '20% MAD',
        y: Array(12).fill(mar * 0.2),
        x: this.monthHeaders.map((h) => h.text),
        line: { color: '#5ab190' }
      }

      const mad20 = {
        type: 'line',
        mode: 'lines',
        hoverinfo: 'skip',
        name: '15% MAD',
        y: Array(12).fill(mar * 0.15),
        x: this.monthHeaders.map((h) => h.text),
        line: { color: '#fec925' }
      }

      const mad10 = {
        type: 'line',
        mode: 'lines',
        hoverinfo: 'skip',
        name: '10% MAD',
        y: Array(12).fill(mar * 0.1),
        x: this.monthHeaders.map((h) => h.text),
        line: { color: '#fa1e44' }
      }

      plotConfig.push(availabilityData, mad10, mad20, mad30)

      if(this.licencePlotData) {
        plotConfig.push({
          type: 'bar',
          name: 'Monthly Licenced Quantity',
          y: this.licencePlotData,
          x: this.monthHeaders.map((h) => h.text),
          hovertemplate: '%{y:.2f} m³'
        })
      }

      if(this.shortTermLicencePlotData) {
        plotConfig.push({
          type: 'bar',
          name: 'Monthly Short Term Approvals Quantity',
          y: this.shortTermLicencePlotData,
          x: this.monthHeaders.map((h) => h.text),
          hovertemplate: '%{y:.2f} m³'
        })
      }

      return plotConfig
    }
  },
  methods: {
    demandAvailabilityLayout () {
      return {
        barmode: 'stack',
        title: 'Availability vs Licenced Quantity',
        showlegend: true,
        legend: {
          xanchor: 'center',
          x: 0.5,
          y: -0.2,
          orientation: 'h'
        },
        margin: {
          r: 120
        },
        xaxis: {
          tickformat: '%B'
        },
        yaxis: {
          title: 'Volume (m³)'
        }
      }
    }
  }
}
</script>

<style>
</style>
