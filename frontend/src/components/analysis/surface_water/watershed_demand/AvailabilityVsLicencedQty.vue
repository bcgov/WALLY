<template>
  <v-card flat>
    <v-card-text class="pb-0">
      <h3>Licensed Quantity</h3>
    </v-card-text>

    <v-card-text v-if="demandAvailabilityData">
      <v-row>
        <v-col>
          <v-card flat outlined tile>
            <v-card-title>
              How to read this graph
            </v-card-title>
            <v-card-text class="info-blue">
              <strong>
                This graph shows allocation from existing surface water licences (including any adjusted monthly allocation values) expressed as withdrawal rate in cubic metres per second (m³/s).
              </strong>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <Plotly v-if="availabilityPlotData && licencePlotData && shortTermLicencePlotData"
                :layout="demandAvailabilityLayout()"
                :data="demandAvailabilityData"
        ></Plotly>
      </v-row>
    </v-card-text>
    <v-card-text v-else>
      No data to display
    </v-card-text>
  </v-card>
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
      var plotConfig = []

      if (this.licencePlotData) {
        plotConfig.push({
          type: 'bar',
          name: 'Monthly Licenced Quantity',
          y: this.licencePlotData.map((v, i) => {
            return v / this.secondsInMonth(i + 1)
          }),
          x: this.monthHeaders.map((h) => h.text),
          hovertemplate: '%{y:.2f} m³/s',
          marker: { color: 'orange' }
        })
      }

      if (this.shortTermLicencePlotData) {
        plotConfig.push({
          type: 'bar',
          name: 'Monthly Short Term Approvals Quantity',
          y: this.shortTermLicencePlotData.map((v, i) => {
            return v / this.secondsInMonth(i + 1)
          }),
          x: this.monthHeaders.map((h) => h.text),
          hovertemplate: '%{y:.2f} m³/s',
          marker: { color: 'purple' }
        })
      }

      return plotConfig
    }
  },
  methods: {
    // return the number of seconds in a given month.
    // Month is represented by an integer, starting with 1 for January.
    secondsInMonth (month) {
      return 60 * 60 * 24 * this.months[month]
    },
    demandAvailabilityLayout () {
      return {
        barmode: 'stack',
        title: 'Licenced quantity (as withdrawal rate)',
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
          title: 'Withdrawal (m³/s)'
        }
      }
    }
  }
}
</script>

<style>
</style>
