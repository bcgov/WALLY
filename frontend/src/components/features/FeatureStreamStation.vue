<template>
  <v-card elevation=0>
    <v-card-text>
      <div class="grey--text text--darken-4 headline" id="stationTitle">{{ record.properties.name }}</div>
      <div class="grey--text text--darken-2 title">Stream monitoring station</div>
      <v-divider></v-divider>
      <div class="grey--text text--darken-4">
        <div v-if="station">Station Number: {{ station.station_number }}</div>
        <div v-if="station">Flow data: {{ formatYears(station.flow_years) }}</div>
        <div v-if="station">Station Status: {{ stationStatus(station.hyd_status) }}</div>
        <div v-if="station">Gross drainage area: {{ station.drainage_area_gross }} km</div>
        <div v-if="station">WSC Historical Link: <a :href="`https://wateroffice.ec.gc.ca/report/historical_e.html?stn=${station.station_number}`"
          target="_blank"
        >{{station.station_number}}</a></div>
        <div v-if="station && station.real_time === 1">WSC Realtime Link: <a :href="`https://wateroffice.ec.gc.ca/report/real_time_e.html?stn=${station.station_number}`"
          target="_blank"
        >{{station.station_number}}</a></div>
      </div>
      <v-list dense class="mx-0 px-0">
        <v-list-item>
          <v-select
            v-model="selectedYear"
            :items="yearOptions"
            :menu-props="{ maxHeight: '400' }"
            label="Select year"
            item-text="label"
            item-value="value"
            hint="Available data in this year"
          ></v-select>
        </v-list-item>
        <v-list-item>
          <v-list-item-content class="mx-0 px-0">
            <Plotly id="flowPlot" :data="plotFlowData" :layout="plotFlowLayout" ref="flowPlot"></Plotly>
          </v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Water levels:</v-list-item-content>
          <v-list-item-content class="align-end" v-if="station">{{ formatYears(station.level_years) }}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <Plotly id="levelPlot" :data="plotLevelData" :layout="plotLevelLayout" ref="levelPlot"></Plotly>
          </v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>
            Source: <a href="https://www.canada.ca/en/environment-climate-change/services/water-overview/quantity/monitoring/survey/data-products-services/national-archive-hydat.html" target="_blank">National Water Data Archive</a>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
import ApiService from '../../services/ApiService'
import EventBus from '../../services/EventBus'
import { SHORT_MONTHS } from '../../constants/dates'
const Plotly = () => import('vue-plotly').then(module => {
  return module.Plotly
})

export default {
  name: 'FeatureStreamStation',
  components: {
    Plotly
  },
  props: {
    record: Object
  },
  data () {
    return {
      loading: false,
      station: null,
      flowData: [],
      levelData: [],
      selectedYear: null,
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
    yearOptions () {
      if (!this.station) { return [] }
      let allOption = [{ label: 'Monthly average all years', value: null }]
      return allOption.concat(this.station.flow_years.map((w, i) => ({
        label: w,
        value: w
      })))
    },
    plotFlowData () {
      const mean = {
        x: this.flowData.map(w => w.month),
        y: this.flowData.map(w => w.monthly_mean),
        text: this.flowData.map(w => w.monthly_mean),
        textposition: 'bottom',
        name: 'Monthly flow (average by month)',
        hovertemplate:
          '<b>Mean</b>: %{text} m³/s',
        mode: 'markers+lines',
        type: 'scatter',
        marker: {
          color: '#1f548a'
        }
      }
      const max = {
        x: this.flowData.map(w => w.month),
        y: this.flowData.map(w => w.max),
        text: this.flowData.map(w => w.max),
        textposition: 'bottom',
        name: 'Monthly flow (max recorded)',
        hovertemplate:
          '<b>Max</b>: %{text} m³/s',
        mode: 'markers+lines',
        type: 'scatter',
        marker: {
          color: '#26A69A'
        }
      }
      const min = {
        x: this.flowData.map(w => w.month),
        y: this.flowData.map(w => w.min),
        text: this.flowData.map(w => w.min),
        textposition: 'bottom',
        name: 'Monthly flow (min recorded)',
        hovertemplate:
          '<b>Min</b>: %{text} m³/s',
        mode: 'markers+lines',
        type: 'scatter',
        marker: {
          color: '#494949'
        }
      }
      return [mean, max, min]
    },
    plotFlowLayout () {
      const opts = {
        shapes: [],
        title: 'Monthly Flow',
        height: 500,
        hovermode: 'closest',
        legend: {
          x: -0.1,
          y: 1.3
        },
        yaxis: {
          title: {
            text: 'Discharge (m³/s)'
          }
        },
        xaxis: {
          title: {
            text: 'Month'
          }
        }
      }
      return opts
    },
    plotLevelData () {
      const mean = {
        x: this.levelData.map(w => w.month),
        y: this.levelData.map(w => w.monthly_mean),
        text: this.levelData.map(w => w.monthly_mean),
        textposition: 'bottom',
        name: 'Water level (average by month)',
        hovertemplate:
          '<b>Mean</b>: %{text} m',
        mode: 'markers+lines',
        type: 'scatter',
        marker: {
          color: '#1f548a'
        }
      }
      const max = {
        x: this.levelData.map(w => w.month),
        y: this.levelData.map(w => w.max),
        text: this.levelData.map(w => w.max),
        textposition: 'bottom',
        name: 'Water level (average by max)',
        hovertemplate:
          '<b>Max</b>: %{text} m',
        mode: 'markers+lines',
        type: 'scatter',
        marker: {
          color: '#26A69A'
        }
      }
      const min = {
        x: this.levelData.map(w => w.month),
        y: this.levelData.map(w => w.min),
        text: this.levelData.map(w => w.min),
        textposition: 'bottom',
        name: 'Water level (average by min)',
        hovertemplate:
          '<b>Min</b>: %{text} m',
        mode: 'markers+lines',
        type: 'scatter',
        marker: {
          color: '#494949'
        }
      }
      return [mean, max, min]
    },
    plotLevelLayout () {
      const opts = {
        shapes: [],
        title: 'Water Level',
        height: 500,
        hovermode: 'closest',
        legend: {
          x: -0.1,
          y: 1.3
        },
        yaxis: {
          title: {
            text: 'Level (m)'
          }
        },
        xaxis: {
          title: {
            text: 'Month'
          }
        }
      }
      return opts
    }
  },
  methods: {
    stationStatus (status) {
      if (status === 'A') {
        return 'Active'
      } else if (status === 'D') {
        return 'Deactivated'
      } else {
        return 'Unknown'
      }
    },
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
        const msg = e.response ? e.response.data.detail : true
        EventBus.$emit('error', msg)
      }).finally(() => {
        this.loading = false
      })
    },
    fetchMonthlyData (flowURL, levelURL) {
      if (this.selectedYear != null) {
        flowURL = flowURL + '?year=' + this.selectedYear
        levelURL = levelURL + '?year=' + this.selectedYear
      }

      ApiService.getRaw(flowURL).then((r) => {
        this.flowData = r.data
        this.flowChartOptions = this.newChartOptions('Discharge (average by month)', 'm³/s', this.flowData.map((x) => [x.max]))
        setTimeout(() => { this.flowChartReady = true }, 0)
      }).catch((e) => {
        const msg = e.response ? e.response.data.detail : true
        EventBus.$emit('error', msg)
      })

      ApiService.getRaw(levelURL).then((r) => {
        this.levelData = r.data
        this.levelChartOptions = this.newChartOptions('Water level (average by month)', 'm', this.levelData.map((x) => [x.max]))
        setTimeout(() => { this.levelChartReady = true }, 0)
      }).catch((e) => {
        const msg = e.response ? e.response.data.detail : true
        EventBus.$emit('error', msg)
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
    selectedYear () {
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
