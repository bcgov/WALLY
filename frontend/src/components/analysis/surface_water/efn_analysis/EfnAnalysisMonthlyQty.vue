<template>
  <v-card flat>
    <v-card-text v-if="availabilityData">
      <v-row>
        <v-col>
          <v-card flat outlined tile>
            <v-card-title>
              How to read this graph
            </v-card-title>
            <v-card-text class="info-blue">
              <strong>
                This graph shows available water
              </strong>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <Plotly v-if="meanMonthlyDischarges"
                :layout="availabilityLayout()"
                :data="availabilityData"
        ></Plotly>
      </v-row>
    </v-card-text>
    <v-card-text v-else>
      No data to display
    </v-card-text>
  </v-card>
</template>

<script>
// import { mapGetters } from 'vuex'
const Plotly = () => import('vue-plotly').then(module => {
  return module.Plotly
})

export default {
  name: 'EfnAnalysisMonthlyQty',
  components: {
    Plotly
  },
  props: ['meanMonthlyDischarges'],
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
    availabilityData () {
      console.log(
        'monthly mad: ',
        this.meanMonthlyDischarges
      )

      if (!this.meanMonthlyDischarges) {
        return null
      }
      var plotConfig = []
      let mad = this.meanMonthlyDischarges.reduce((a, b) => a + b, 0) / 12

      const availabilityData = {
        type: 'bar',
        name: 'Available Water',
        y: this.meanMonthlyDischarges,
        x: this.monthHeaders.map((h) => h.text),
        hovertemplate: '%{y:.2f} m³/s'
      }

      const mad30 = {
        type: 'line',
        mode: 'lines',
        hoverinfo: 'skip',
        name: '20% MAD',
        y: Array(12).fill(mad * 0.2),
        x: this.monthHeaders.map((h) => h.text),
        line: { color: '#5ab190' }
      }

      const mad20 = {
        type: 'line',
        mode: 'lines',
        hoverinfo: 'skip',
        name: '15% MAD',
        y: Array(12).fill(mad * 0.15),
        x: this.monthHeaders.map((h) => h.text),
        line: { color: '#fec925' }
      }

      const mad10 = {
        type: 'line',
        mode: 'lines',
        hoverinfo: 'skip',
        name: '10% MAD',
        y: Array(12).fill(mad * 0.1),
        x: this.monthHeaders.map((h) => h.text),
        line: { color: '#fa1e44' }
      }

      plotConfig.push(availabilityData, mad10, mad20, mad30)

      return plotConfig
    }
  },
  methods: {
    availabilityLayout () {
      return {
        barmode: 'stack',
        title: 'EFN Availability',
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
          title: 'Discharge (m³/s)'
        }
      }
    }
  }
}
</script>

<style>
</style>
