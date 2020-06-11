<template>
  <div>
    <div class="title my-5">Climate Data</div>
    <div v-if="climateDataLoading">
      <v-progress-linear show indeterminate></v-progress-linear>
    </div>
    <div v-if="climateData">
      <div class="mt-3">
        <span class="font-weight-bold">Glacial coverage:</span> {{ climateData.glacial_area.toFixed(1) }} sq. m ({{(climateData.glacial_coverage * 100).toFixed(1)}}%)
      </div>
      <div class="my-3" v-if="potentialEvapotranspiration">
        <div>
          <span class="font-weight-bold">Potential evapotranspiration</span>
        </div>
        <div>
          <span>Hamon equation:</span> {{ potentialEvapotranspiration.hamon.toFixed(1) }} mm/yr
        </div>
        <div>
          <span>Thornthwaite method:</span> {{ potentialEvapotranspiration.thornthwaite.toFixed(1) }} mm/yr
        </div>
      </div>
      <div v-if="precipData">
        <div class="title mt-5">Precipitation</div>
        <Plotly :data="precipData" :layout="precipLayout"/>
        <v-row align="center">
          <v-col cols=12 md=8>
            Source: <a href="https://pacificclimate.org/analysis-tools/pcic-climate-explorer" target="_blank">Pacific Climate Impacts Consortium - Climate Explorer</a>
          </v-col>
          <v-col cols=12 md=4><v-btn small color="blue-grey lighten-4">Export GeoJSON shape</v-btn></v-col>
        </v-row>
        <v-row>
          <v-col>
            Note: precipitation search area is {{ (climateData.precip_search_area / climateData.projected_geometry_area * 100).toFixed(1) }}% of the watershed area.
          </v-col>
        </v-row>
      </div>
    </div>
  </div>
</template>

<script>
import ApiService from '../../../services/ApiService'
const Plotly = () => import('vue-plotly').then(module => {
  return module.Plotly
})

export default {
  name: 'WatershedClimate',
  props: ['watershedID', 'record'],
  components: {
    Plotly
  },
  data: () => ({
    climateData: null,
    climateDataLoading: false,
    precipLayout: {
      title: 'Precipitation (1981-2010)',
      xaxis: {
        tickformat: '%B'
      },
      yaxis: {
        title: 'mm/day'
      }
    }
  }),
  watch: {
    watershedID () {
      this.climateData = null
      this.fetchClimateData()
    }
  },
  computed: {
    potentialEvapotranspiration () {
      return {
        hamon: this.climateData.potential_evapotranspiration_hamon,
        thornthwaite: this.climateData.potential_evapotranspiration_thornthwaite
      }
    },
    precipData () {
      if (!this.climateData || !this.climateData.precipitation) {
        return null
      }

      const plotData = {
        type: 'scatter',
        mode: 'lines',
        name: 'Precipitation (1981-2010)',
        y: Object.values(this.climateData.precipitation.data),
        x: Object.keys(this.climateData.precipitation.data),
        line: { color: '#17BECF' }
      }
      return [plotData]
    }
  },
  methods: {
    fetchClimateData () {
      this.climateDataLoading = true
      ApiService.query(`/api/v1/watersheds/${this.watershedID}`)
        .then(r => {
          this.climateData = r.data
          this.climateDataLoading = false
        })
        .catch(e => {
          this.climateDataLoading = false
          console.error(e)
        })
    }
  },
  mounted () {
    this.fetchClimateData()
  }
}
</script>

<style>

</style>
