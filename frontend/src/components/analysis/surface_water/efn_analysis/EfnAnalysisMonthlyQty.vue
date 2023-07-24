<template>
  <v-card flat>
    <v-card-text>
      <v-row>
        <v-col>
          <v-card flat outlined tile>
            <v-card-title>
              How to read this graph
            </v-card-title>
            <v-card-text class="info-blue">
              <strong>
                This graph shows available water vs the licenced total withdrawal and the EFN risk levels for each month.
              </strong>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <Plotly
          :layout="availabilityLayout()"
          :data="availabilityData"
        ></Plotly>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
const Plotly = () => import('vue-plotly').then(module => {
  return module.Plotly
})

export default {
  name: 'EfnAnalysisMonthlyQty',
  components: {
    Plotly
  },
  props: ['mmd', 'mad', 'riskLevels', 'licenceData'],
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
      if (!this.mmd) {
        return null
      }
      var plotConfig = []

      const availabilityData = {
        type: 'bar',
        name: 'Available Water',
        marker: {
          color: '#095599'
        },
        y: this.mmd.map((val, i) => {
          let availability = val - (this.licenceData.longTerm ? this.licenceData.longTerm[i] : 0) -
              (this.licenceData.shortTerm ? this.licenceData.shortTerm[i] : 0)
          if (availability < 0) {
            availability = 0
          }
          return availability
        }),
        x: this.monthHeaders.map((h) => h.text),
        hovertemplate: '%{y:.2f} m³/s'
      }

      const longTerm = {
        type: 'bar',
        name: 'Monthly Licenced Quantity',
        y: this.licenceData.longTerm,
        x: this.monthHeaders.map((h) => h.text),
        hovertemplate: '%{y:.2f} m³/s',
        marker: { color: '#8377D1' }
      }

      const shortTerm = {
        type: 'bar',
        name: 'Monthly Short Term Approvals Quantity',
        y: this.licenceData.shortTerm,
        x: this.monthHeaders.map((h) => h.text),
        hovertemplate: '%{y:.2f} m³/s',
        marker: { color: 'purple' }
      }

      const high = {
        type: 'line',
        marker: {
          color: '#EF2917'
        },
        line: {
          color: '#EF2917',
          width: 1
        },
        hoverinfo: 'skip',
        name: 'High Risk',
        y: this.mmd.map((val, i) => {
          return val * this.riskLevels[i][1]
        }),
        x: this.monthHeaders.map((h) => h.text)
      }

      const moderate = {
        type: 'line',
        marker: {
          color: '#EFA00B'
        },
        line: {
          color: '#EFA00B',
          width: 1
        },
        hoverinfo: 'skip',
        name: 'Moderate Risk',
        y: this.mmd.map((val, i) => {
          return val * this.riskLevels[i][0]
        }),
        x: this.monthHeaders.map((h) => h.text)
      }

      const mad20 = {
        type: 'line',
        mode: 'lines',
        hoverinfo: 'skip',
        name: '20% MAD',
        y: Array(12).fill(this.mad * 0.2),
        x: this.monthHeaders.map((h) => h.text),
        line: { color: '#5ab190' }
      }

      const mad10 = {
        type: 'line',
        mode: 'lines',
        hoverinfo: 'skip',
        name: '10% MAD',
        y: Array(12).fill(this.mad * 0.1),
        x: this.monthHeaders.map((h) => h.text),
        line: { color: '#fec925' }
      }

      // const low = {
      //   type: 'line',
      //   marker: {
      //     color: '#62C370'
      //   },
      //   line: {
      //     color: '#62C370',
      //     width: 1
      //   },
      //   hoverinfo: 'skip',
      //   name: 'Low Risk',
      //   y: this.riskLevels.map(rl => rl[0]),
      //   x: this.monthHeaders.map((h) => h.text)
      // }

      plotConfig.push(moderate, high, shortTerm, longTerm, availabilityData, mad10, mad20)

      return plotConfig
    }
  },
  methods: {
    availabilityLayout () {
      return {
        barmode: 'stack',
        title: 'EFN Risk vs Availability',
        showlegend: true,
        legend: {
          xanchor: 'center',
          x: 0.5,
          y: -0.2,
          orientation: 'h'
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
