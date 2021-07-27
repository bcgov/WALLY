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
        <div v-if="station">Gross drainage area: {{ station.drainage_area_gross ? `${station.drainage_area_gross.toFixed(1)} km²` : "N/A" }}</div>
        <div v-if="station">WSC Historical Link: <a :href="`https://wateroffice.ec.gc.ca/report/historical_e.html?stn=${station.station_number}`"
          target="_blank"
        >{{station.station_number}}</a></div>
        <div v-if="station && station.real_time === 1">WSC Realtime Link: <a :href="`https://wateroffice.ec.gc.ca/report/real_time_e.html?stn=${station.station_number}`"
          target="_blank"
        >{{station.station_number}}</a></div>
      </div>
      <v-list dense class="mx-0 px-0">
        <v-list-item>
          <!-- TODO: fix year selection.  Must filter FASSTR data by year. -->
          <!-- <v-select
            v-model="selectedYear"
            :items="yearOptions"
            :menu-props="{ maxHeight: '400' }"
            label="Select year"
            item-text="label"
            item-value="value"
            hint="Available data in this year"
          ></v-select> -->
        </v-list-item>
        <v-list-item>
          <v-list-item-content class="mx-0 px-0">
            <div v-if="flowDataLoading">
              <v-progress-linear show indeterminate></v-progress-linear>
            </div>
            <Plotly id="flowPlot" :data="plotFlowData" :layout="plotFlowLayout" ref="flowPlot"></Plotly>
          </v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Water levels:</v-list-item-content>
          <v-list-item-content class="align-end" v-if="station && levelData && levelData.length">{{ formatYears(station.level_years) }}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <div v-if="levelDataLoading">
              <v-progress-linear show indeterminate></v-progress-linear>
            </div>
            <div v-if="levelData && levelData.length">
              <Plotly id="levelPlot" :data="plotLevelData" :layout="plotLevelLayout" ref="levelPlot"></Plotly>
            </div>
            <div v-else>
              <p>No water level data for this station.</p>
            </div>
          </v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>
            <p>
              Source: <a href="https://www.canada.ca/en/environment-climate-change/services/water-overview/quantity/monitoring/survey/data-products-services/national-archive-hydat.html" target="_blank">National Water Data Archive</a>
            </p>
            <p>
              Flow and low flow statistics computed using <a href="https://github.com/bcgov/fasstr" target="_blank">FASSTR</a>.
            </p>
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
      flowDataLoading: false,
      levelData: [],
      levelDataLoading: false,
      flowStats: null,
      flowStatsError: null,
      flowStatsLoading: false,
      selectedYear: null,
      levelChartOptions: {},
      flowChartReady: false,
      levelChartReady: false,
      flowStatsHeaders: [
        { text: 'Name', value: 'display_name' },
        { text: 'Discharge (m³/s)', value: 'value' }
      ],
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
      if (!this.flowData || !this.flowData.months) {
        return []
      }

      // light blue  dark blue  light yellow  dark red  dark yellow  light red
      const mad = {
        type: 'line',
        mode: 'lines',
        hoverinfo: 'skip',
        name: 'Mean Annual Discharge (m³/s)',
        y: Array(12).fill(this.flowData.mean),
        x: this.monthHeaders.map((h) => h.text),
        text: Array(12).fill(this.flowData.mean.toFixed(2)),
        textposition: 'bottom',
        hovertemplate:
          '<b>Mean annual discharge</b>: %{text} m³/s',
        line: { color: '#494949' }
      }
      const mean = {
        x: this.flowData.months.map(w => w.month),
        y: this.flowData.months.map(w => w.mean),
        text: this.flowData.months.map(w => w.mean.toFixed(2)),
        textposition: 'bottom',
        name: 'Monthly flow (average by month)',
        hovertemplate:
          '<b>Mean</b>: %{text} m³/s',
        mode: 'markers+lines',
        type: 'scatter',
        marker: {
          color: '#003f5c'
        }
      }
      const max = {
        x: this.flowData.months.map(w => w.month),
        y: this.flowData.months.map(w => w.maximum),
        text: this.flowData.months.map(w => w.maximum.toFixed(2)),
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
        x: this.flowData.months.map(w => w.month),
        y: this.flowData.months.map(w => w.minimum),
        text: this.flowData.months.map(w => w.minimum.toFixed(2)),
        textposition: 'bottom',
        name: 'Monthly flow (min recorded)',
        hovertemplate:
          '<b>Min</b>: %{text} m³/s',
        mode: 'markers+lines',
        type: 'scatter',
        marker: {
          color: '#26A69A'
        }
      }
      const p10 = {
        x: this.flowData.months.map(w => w.month),
        y: this.flowData.months.map(w => w.p10),
        text: this.flowData.months.map(w => w.p10.toFixed(2)),
        textposition: 'bottom',
        name: 'P10',
        hovertemplate:
          '<b>P10</b>: %{text} m³/s',
        mode: 'markers+lines',
        type: 'scatter',
        marker: {
          color: '#1f548a'
        }
      }
      const p90 = {
        x: this.flowData.months.map(w => w.month),
        y: this.flowData.months.map(w => w.p90),
        text: this.flowData.months.map(w => w.p90.toFixed(2)),
        textposition: 'bottom',
        name: 'P90',
        hovertemplate:
          '<b>P90</b>: %{text} m³/s',
        mode: 'markers+lines',
        type: 'scatter',
        marker: {
          color: '#1f548a'
        }
      }
      return [mean, max, min, mad, p10, p90]
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
    },
    flowStatsItems () {
      // formats flow stats as an array of objects e.g [{ name: "Low 7Q10", value: "1.5", units: "m3/s" }, ...]

      if (!this.flowStats || !this.flowStats.stats) {
        return []
      }

      return this.flowStats.stats
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
      this.levelChartOptions = {}
      this.flowStatsLoading = false
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
      this.flowDataLoading = true
      ApiService.getRaw(flowURL).then((r) => {
        this.flowData = r.data
        setTimeout(() => { this.flowChartReady = true }, 0)
      }).catch((e) => {
        const msg = e.response ? e.response.data.detail : true
        EventBus.$emit('error', msg)
      }).finally(() => {
        this.flowDataLoading = false
      })

      this.levelDataLoading = true
      ApiService.getRaw(levelURL).then((r) => {
        this.levelData = r.data
        this.levelChartOptions = this.newChartOptions('Water level (average by month)', 'm', this.levelData.map((x) => [x.max]))
        setTimeout(() => { this.levelChartReady = true }, 0)
      }).catch((e) => {
        const msg = e.response ? e.response.data.detail : true
        EventBus.$emit('error', msg)
      }).finally(() => {
        this.levelDataLoading = false
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
    },
    record: {
      deep: true,
      handler () {
        this.fetchRecord()
      }
    }
  },
  mounted () {
    this.fetchRecord()
  }
}
</script>

<style>
</style>
