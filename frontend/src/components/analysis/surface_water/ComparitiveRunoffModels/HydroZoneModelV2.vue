<template>
  <div>
    <v-card-text v-if="showWallyModelFeatureFlag && modelData">
      <v-card-actions>
        <v-card-subtitle class="pr-0 pl-2 pr-2">
          Source:
        </v-card-subtitle>
        Wally Hydrological Zone Model V2
      </v-card-actions>
      <v-row class="pl-3 pr-3">
        <v-col>
          <v-card flat outlined tile height="100%">
            <v-card-title>
              Mean Annual Runoff Estimate:
              <v-icon small class="ml-1">mdi-information-outline</v-icon>
            </v-card-title>
            <v-card-text class="info-blue">
              <strong>{{ meanAnnualFlow }} m^3/sec</strong>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col>
          <v-card flat outlined tile height="100%">
            <v-card-title>
              Model R Squared:
              <v-icon small class="ml-1">mdi-information-outline</v-icon>
            </v-card-title>
            <v-card-text class="info-blue">
              <strong>{{ meanAnnualFlowRSquared }}</strong>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-card-text>
    <Plotly v-if="meanMonthlyPlotData"
            :layout="meanMonthlyLayout"
            :data="meanMonthlyPlotData"
    ></Plotly>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import qs from 'querystring'
import ApiService from '../../../../services/ApiService'

const Plotly = () => import('vue-plotly').then(module => {
  return module.Plotly
})
const months = [
  '2020-01-01',
  '2020-02-01',
  '2020-03-01',
  '2020-04-01',
  '2020-05-01',
  '2020-06-01',
  '2020-07-01',
  '2020-08-01',
  '2020-09-01',
  '2020-10-01',
  '2020-11-01',
  '2020-12-01'
]

export default {
  name: 'HydroZoneModelV2',
  components: {
    Plotly
  },
  props: {
    record: null,
    allWatersheds: {
      type: Array,
      default: () => ([])
    },
    surface_water_design_v2: null
  },
  data: () => ({
    monthlyRunoffCoefficients: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    meanMonthlyLayout: {
      title: 'Mean Monthly Flows',
      legend: {
        xanchor: 'center',
        x: 0.5,
        y: -0.1,
        orientation: 'h'
      },
      xaxis: {
        tickformat: '%B'
      },
      yaxis: {
        title: 'm³/s'
      }
    },
    modelData: {},
    modelLoading: false
  }),
  computed: {
    ...mapGetters('surfaceWater', ['watershedDetails']),
    watershedArea () {
      if (!this.record || !this.record.properties['FEATURE_AREA_SQM']) {
        return null
      }
      return Number(this.record.properties['FEATURE_AREA_SQM'])
    },
    meanMonthlyPlotData () {
      var flowData = this.meanMonthlyFlows()
      if (!flowData) {
        return null
      }
      const plotData = {
        type: 'bar',
        name: 'm3^s',
        y: flowData,
        x: months,
        line: { color: '#17BECF' }
      }

      const mad20 = {
        type: 'line',
        name: '20% MAD',
        y: flowData.map(f => f * 0.2),
        x: months,
        line: { color: '#17BECF' }
      }

      const mad10 = {
        type: 'line',
        name: '10% MAD',
        y: flowData.map(f => f * 0.1),
        x: months,
        line: { color: '#17BECF' }
      }

      return [plotData, mad20, mad10]
    },
    meanAnnualFlow () {
      if (this.modelData && this.modelData.mean_annual_flow && this.modelData.mean_annual_flow.mean_annual_flow) {
        return Number(this.modelData.mean_annual_flow.mean_annual_flow).toFixed(2)
      }
      return null
    },
    meanAnnualFlowRSquared () {
      if (this.modelData && this.modelData.mean_annual_flow && this.modelData.mean_annual_flow.r_squared) {
        return Number(this.modelData.mean_annual_flow.r_squared).toFixed(2)
      }
      return null
    }
  },
  methods: {
    meanMonthlyFlows () {
      if (this.modelData && this.modelData.mean_monthly_flows) {
        var meanMonthlyFlows = this.modelData.mean_monthly_flows.map((flow) => {
          return flow.mean_monthly_flow
        })
        return meanMonthlyFlows
      }
      return []
    },
    fetchWatershedModel (details) {
      console.log(details)
      this.modelLoading = true
      // const params = {
      //   hydrological_zone: details.hydrological_zone,
      //   drainage_area: details.drainage_area,
      //   annual_precipitation: details.annual_precipitation,
      //   glacial_coverage: details.glacial_coverage,
      //   glacial_area: details.glacial_area
      // }
      // console.log(params)
      details['year'] = new Date().getFullYear()
      ApiService.post('/api/v1/hydrological_zones/v2_watershed_drainage_model', details)
        .then(r => {
          this.modelData = r.data
          this.modelLoading = false
        })
        .catch(e => {
          this.modelLoading = false
          console.error(e)
        })
    },
    showWallyModelFeatureFlag () {
      return this.app && this.app.config && this.app.config.wally_model
    }
  },
  mounted () {
  },
  watch: {
    watershedDetails: {
      immediate: true,
      handler (val, oldVal) {
        this.fetchWatershedModel(val)
      }
    }
  }
}
</script>

<style>
</style>
