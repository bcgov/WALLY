<template>
  <div>
    <div v-if="watershedDetails">
      <div class="title my-5">Climate Data</div>
      <div class="my-3">
        <span class="font-weight-bold">Glacial coverage:</span> {{ watershedDetails.glacial_area.toFixed(1) }} sq. m ({{(watershedDetails.glacial_coverage * 100).toFixed(1)}}%)
      </div>
      <div v-if="precipData">
        <div class="title mt-5">Precipitation</div>
        <Chart :data="precipData" :layout="precipLayout"/>
        <v-row align="center">
          <v-col cols=12 md=8>
            Source: <a href="https://pacificclimate.org/analysis-tools/pcic-climate-explorer" target="_blank">Pacific Climate Impacts Consortium - Climate Explorer</a>
          </v-col>
          <v-col cols=12 md=4><v-btn small color="blue-grey lighten-4">Export GeoJSON shape</v-btn></v-col>
        </v-row>
        <v-row>
          <v-col>
            Note: precipitation search area is {{ (watershedDetails.precip_search_area / watershedDetails.projected_geometry_area * 100).toFixed(1) }}% of the watershed area.
          </v-col>
        </v-row>
      </div>
    </div>
  </div>
</template>

<script>
import ApiService from '../../../services/ApiService'
import Chart from '../../charts/Chart'
export default {
  name: 'WatershedClimate',
  props: ['watershedID', 'record'],
  components: {
    Chart
  },
  data: () => ({
    watershedDetails: null,
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
      this.watershedDetails = null
      this.fetchWatershedDetails()
    }
  },
  computed: {
    precipData () {
      if (!this.watershedDetails || !this.watershedDetails.precipitation) {
        return null
      }

      const plotData = {
        type: 'scatter',
        mode: 'lines',
        name: 'Precipitation (1981-2010)',
        y: Object.values(this.watershedDetails.precipitation.data),
        x: Object.keys(this.watershedDetails.precipitation.data),
        line: { color: '#17BECF' }
      }
      return [plotData]
    }
  },
  methods: {
    fetchWatershedDetails () {
      ApiService.query(`/api/v1/watersheds/${this.watershedID}`)
        .then(r => {
          this.watershedDetails = r.data
        })
        .catch(e => {
          console.error(e)
        })
    }
  },
  mounted () {
    this.fetchWatershedDetails()
  }
}
</script>

<style>

</style>
