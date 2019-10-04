<template>
  <v-card elevation=0>
    <v-card-text>
      <div class="grey--text text--darken-4 title" id="stationTitle">{{ record.properties.name }}</div>
      <div class="grey--text text--darken-2 subtitle-1">Stream monitoring station</div>
      <v-divider></v-divider>
      <v-list dense class="mx-0 px-0" v-if="station">
        <v-list-item>
          <v-list-item-content>Flow data:</v-list-item-content>
          <v-list-item-content class="align-end">{{ formatYears(station.flow_years) }}</v-list-item-content>
        </v-list-item>
        <v-list-item v-if="station.flow_years && station.flow_years.length">
          <v-list-item-content class="mx-0 px-0">
            <line-chart v-if="flowChartReady" :chartData="flowChartData" :options="flowChartOptions"></line-chart>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Water levels:</v-list-item-content>
          <v-list-item-content class="align-end">{{ formatYears(station.level_years) }}</v-list-item-content>
        </v-list-item>
        <v-list-item v-if="station.level_years && station.level_years.length">
          <v-list-item-content>
            <line-chart v-if="levelChartReady" :chartData="levelChartData" :options="levelChartOptions"></line-chart>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            Source: <a href="https://www.canada.ca/en/environment-climate-change/services/water-overview/quantity/monitoring/survey/data-products-services/national-archive-hydat.html" target="_blank">National Water Data Archive</a>
          </v-list-item-content>
        </v-list-item>
        <!-- <v-list-item class="mt-3">
          <v-list-item-content>
            <a href="#">How is this information calculated?</a>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <a href="#">Improve this feature</a>
          </v-list-item-content>
        </v-list-item> -->
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
import ApiService from '../../services/ApiService'
import { LineChart } from '../chartjs/Charts'
import { SHORT_MONTHS } from '../../constants/dates'

export default {
  name: 'FeatureStreamStation',
  components: {
    LineChart
  },
  props: {
    record: Object
  },
  data () {
    return {
      loading: false,
      station: {},
      flowChartOptions: {},
      levelChartOptions: {},
      flowChartReady: false,
      levelChartReady: false
    }
  },
  computed: {
    recordEndpoint () {
      return this.record.properties.url
    },
    flowChartData () {
      if (!this.flowData || !this.flowChartReady) {
        return { datasets: [] }
      }
      return {
        datasets: [
          {
            label: 'Daily flow (average by month)',
            lineTension: 0,
            fill: false,
            borderColor: '#1f548a',
            data: this.flowData.map((o) => ({
              x: o.month,
              y: o.monthly_mean
            }))
          },
          {
            label: 'Daily flow (max recorded)',
            lineTension: 0,
            fill: false,
            borderColor: '#26A69A',
            data: this.flowData.map((o) => ({
              x: o.month,
              y: o.max
            }))
          },
          {
            label: 'Daily flow (min recorded)',
            lineTension: 0,
            fill: false,
            borderColor: '#494949',
            data: this.flowData.map((o) => ({
              x: o.month,
              y: o.min
            }))
          }
        ]
      }
    },
    levelChartData () {
      if (!this.levelData || !this.levelChartReady) {
        return { datasets: [] }
      }
      return {
        datasets: [
          {
            label: 'Water level (average by month)',
            lineTension: 0,
            fill: false,
            borderColor: '#1f548a',
            data: this.levelData.map((o) => ({
              x: o.month,
              y: o.monthly_mean
            }))
          },
          {
            label: 'Water level (max recorded)',
            lineTension: 0,
            fill: false,
            borderColor: '#26A69A',
            data: this.levelData.map((o) => ({
              x: o.month,
              y: o.max
            }))
          },
          {
            label: 'Water level (min recorded)',
            lineTension: 0,
            fill: false,
            borderColor: '#494949',
            data: this.levelData.map((o) => ({
              x: o.month,
              y: o.min
            }))
          }
        ]
      }
    }
  },
  methods: {
    resetStation () {
      this.station = null
      this.flowChartReady = false
      this.levelChartReady = false
      this.flowData = []
      this.levelData = []
      this.flowChartOptions = {}
      this.levelChartOptions = {}
    },
    fetchRecord () {
      this.loading = true
      this.resetStation()

      ApiService.getRaw(this.record.properties.url).then((r) => {
        this.station = r.data
        this.fetchMonthlyData(this.station.stream_flows_url, this.station.stream_levels_url)
      }).catch((e) => {
        this.error = e
        console.error(e)
      }).finally(() => {
        this.loading = false
      })
    },
    fetchMonthlyData (flowURL, levelURL) {
      ApiService.getRaw(flowURL).then((r) => {
        this.flowData = r.data
        this.flowChartOptions = this.newChartOptions('Discharge (average by month)', 'm3/s', this.flowData.map((x) => [x.max]))
        setTimeout(() => { this.flowChartReady = true }, 0)
      }).catch((e) => {
        console.error(e)
      })

      ApiService.getRaw(levelURL).then((r) => {
        this.levelData = r.data
        this.levelChartOptions = this.newChartOptions('Water level (average by month)', 'm', this.levelData.map((x) => [x.max]))
        setTimeout(() => { this.levelChartReady = true }, 0)
      }).catch((e) => {
        console.error(e)
      })
    },
    formatYears (val) {
      const years = val || []
      if (!years.length) {
        return 'Not available'
      }
      const min = Math.min.apply(Math, years)
      const max = Math.max.apply(Math, years)
      return `${years.length} year${years.length === 1 ? '' : 's'} between ${min} and ${max}`
    },
    newChartOptions (title, units, yValues) {
      return {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          yAxes: [{
            type: 'linear',
            ticks: {
              min: 0,
              max: Math.floor(Math.max.apply(Math, yValues) + 1),
              callback: function (value, index, values) {
                return `${value} ${units}`
              }
            }
          }],
          xAxes: [{
            type: 'linear',
            ticks: {
              min: 0,
              max: 12,
              callback: (value, index, values) => {
                return SHORT_MONTHS[value - 1]
              }
            }
          }]
        }
      }
    }
  },
  watch: {
    recordEndpoint () {
      this.fetchRecord()
    }
  },
  mounted () {
    this.fetchRecord()
  }
}
</script>

<style>

</style>
