<template>
  <v-card flat v-if="this.surface_water_design_v2">
    <v-card-title
      class="title mt-5 ml-3 mr-3 pa-1 mb-2"
      dark>
      Comparative Runoff Models
    </v-card-title>
    <div v-if="showWallyModelFeatureFlag">
      <HydroZoneModelV1 />
      <HydroZoneModelV2 />
    </div>

    <v-card-text v-if="annualNormalizedRunoff">
      <v-card-actions>
        <v-card-subtitle class="pr-0 pl-2 pr-2">
          Source:
        </v-card-subtitle>
        <a href="https://catalogue.data.gov.bc.ca/dataset/hydrology-hydrometric-watershed-boundaries"
           target="_blank" ref="external">
          Hydrometric Watersheds (DataBC)
        </a>
      </v-card-actions>
      <v-row class="pl-3 pr-3">
        <v-col>
          <v-card flat outlined tile height="100%">
            <v-card-title>
              Annual normalized runoff
              <v-icon small class="ml-1">mdi-information-outline</v-icon>
            </v-card-title>
            <v-card-text class="info-blue">
              <strong>{{ annualNormalizedRunoff }} mm</strong>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col>
          <v-card flat outlined tile height="100%">
            <v-card-title>
              Watershed area (highlighted area)
              <v-icon small class="ml-1">mdi-information-outline</v-icon>
            </v-card-title>
            <v-card-text class="info-blue">
              <strong>{{ record && record.properties['FEATURE_AREA_SQM'].toFixed(1) }} sq. m</strong>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row class="pl-3 pr-3">
        <v-col>
          <v-card flat outlined tile>
            <v-card-title>
              Using normalized runoff from
              <v-icon small class="ml-1">mdi-information-outline</v-icon>
            </v-card-title>
            <v-card-text class="info-blue">
              <strong>{{ annualNormalizedRunoffSource }}</strong>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <Plotly v-if="normalizedRunoffByMonth"
              :layout="runoffLayout"
              :data="normalizedRunoffByMonth"
      ></Plotly>
    </v-card-text>
    <!-- TODO remove isolines at future date once confirmed to be not needed -->
    <!-- <v-card-text v-if="annualNormalizedRunoff && annualIsolineRunoff">
      <v-divider class="mt-3 mb-3"></v-divider>
    </v-card-text>
    <v-card-text v-if="annualIsolineRunoff">
      <v-card-actions>
        <v-card-subtitle class="pr-0 pl-2 pr-2">
          Source:
        </v-card-subtitle>
        <a rel="noopener external"
           target="_blank"
           href="https://catalogue.data.gov.bc.ca/dataset/hydrology-normal-annual-runoff-isolines-1961-1990-historical">
          Hydrology: Normal Annual Runoff Isolines (1961 - 1990) - Historical (DataBC)
        </a>
      </v-card-actions>
      <v-row class="pl-3 pr-3">
        <v-col>
          <v-card flat outlined tile height="100%">
            <v-card-title>
              Average annual runoff (by isolines):
              <v-icon small class="ml-1">mdi-information-outline</v-icon>
            </v-card-title>
            <v-card-text class="info-blue">
              <strong>{{ annualIsolineRunoff }} mm</strong>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col>
          <v-card flat outlined tile height="100%">
            <v-card-title>
              Watershed area
              <v-icon small class="ml-1">mdi-information-outline</v-icon>
            </v-card-title>
            <v-card-text class="info-blue">
              <strong>{{ record.properties['FEATURE_AREA_SQM'].toFixed(2) }} sq. m</strong>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <Plotly v-if="isolineRunoffByMonth"
              :layout="isolineRunoffLayout"
              :data="isolineRunoffByMonth">
      </Plotly>
    </v-card-text>
    <v-card-text v-else-if="!fishLoading">
      <p class="text--disabled mt-2">Unknown fish presence</p>
    </v-card-text> -->
  </v-card>
  <div v-else>
    <div>
      <div class="titleSub">Comparative Runoff Models</div>
      <div v-if="showWallyModelFeatureFlag">
        <HydroZoneModelV1 />
        <HydroZoneModelV2 />
      </div>
      <div v-if="annualNormalizedRunoff">
        <div>
          Source:
          <a href="https://catalogue.data.gov.bc.ca/dataset/hydrology-hydrometric-watershed-boundaries" target="_blank">
            Hydrometric Watersheds (DataBC)
          </a>
        </div>
        <div>Annual normalized runoff: {{ annualNormalizedRunoff }} mm</div>
        <div>Watershed area (highlighted area): {{ record.properties['FEATURE_AREA_SQM'].toFixed(1) }} sq. m</div>
        <div>
          Using normalized runoff from: {{ annualNormalizedRunoffSource }}
        </div>
        <Plotly v-if="normalizedRunoffByMonth"
          :layout="runoffLayout"
          :data="normalizedRunoffByMonth"
        ></Plotly>
      </div>
      <!-- TODO remove isolines at future date once confirmed to be not needed -->
      <!-- <div v-if="annualIsolineRunoff">
        <div>
          Source:
          <a href="https://catalogue.data.gov.bc.ca/dataset/hydrology-normal-annual-runoff-isolines-1961-1990-historical" target="_blank">
            Hydrology: Normal Annual Runoff Isolines (1961 - 1990) - Historical (DataBC)
          </a>
        </div>
        <div>Average annual runoff (by isolines): {{ annualIsolineRunoff }} mm</div>
        <div>Watershed area: {{ record.properties['FEATURE_AREA_SQM'].toFixed(2) }} sq. m</div>
        <Plotly v-if="isolineRunoffByMonth"
          :layout="isolineRunoffLayout"
          :data="isolineRunoffByMonth"
        ></Plotly>
      </div> -->
    </div>
    <!-- <div v-if="!annualIsolineRunoff && !annualNormalizedRunoff">No availability models available at this location.</div> -->
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import HydroZoneModelV1 from './ComparitiveRunoffModels/HydroZoneModelV1'
import HydroZoneModelV2 from './ComparitiveRunoffModels/HydroZoneModelV2'

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
  name: 'ComparativeRunoffModels',
  components: {
    Plotly,
    HydroZoneModelV1,
    HydroZoneModelV2
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
    runoffLayout: {
      title: 'Runoff (Normalized annual runoff * area)',
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
    }
    // TODO remove isolines at future date once confirmed to be not needed
    // isolineRunoffLayout: {
    //   title: 'Monthly discharge (using 1961 - 1990 runoff isolines)',
    //   legend: {
    //     xanchor: 'center',
    //     x: 0.5,
    //     y: -0.1,
    //     orientation: 'h'
    //   },
    //   xaxis: {
    //     tickformat: '%B'
    //   },
    //   yaxis: {
    //     title: 'm³/s'
    //   }
    // }
  }),
  watch: {
  },
  computed: {
    ...mapGetters('surfaceWater', ['watershedDetails']),
    ...mapGetters(['app']),
    watershedArea () {
      if (!this.record || !this.record.properties['FEATURE_AREA_SQM']) {
        return null
      }
      return Number(this.record.properties['FEATURE_AREA_SQM'])
    },
    normalizedRunoffByMonth () {
      if (!this.annualNormalizedRunoff || !this.watershedArea) {
        return null
      }
      const meanAnnualDischarge = this.annualNormalizedRunoff * this.watershedArea / 1000 / 365 / 24 / 60 / 60
      const plotData = {
        type: 'bar',
        name: 'MAD',
        y: this.monthlyRunoffCoefficients.map((x) => x * meanAnnualDischarge),
        x: months,
        line: { color: '#17BECF' }
      }

      const mad20 = {
        type: 'line',
        name: '20% MAD',
        y: Array(12).fill(0.2 * meanAnnualDischarge),
        x: months,
        line: { color: '#17BECF' }
      }

      const mad10 = {
        type: 'line',
        name: '10% MAD',
        y: Array(12).fill(0.1 * meanAnnualDischarge),
        x: months,
        line: { color: '#17BECF' }
      }

      return [plotData, mad20, mad10]
    },

    annualNormalizedRunoffSource () {
      const hydroWatershed = this.allWatersheds.find((ws) => {
        return ws.properties['ANNUAL_RUNOFF_IN_MM']
      })

      if (hydroWatershed) {
        return hydroWatershed.properties['SOURCE_NAME']
      }
      return null
    },

    annualNormalizedRunoff () {
      // all watersheds in the area are checked for an annual normalized runoff.
      // this value is inferred from hydrometric stations and is only available
      // for watersheds in the Hydrometric Watersheds dataset. It leads to a rough estimate
      // only.

      const hydroWatershed = this.allWatersheds.find((ws) => {
        return ws.properties['ANNUAL_RUNOFF_IN_MM']
      })

      if (hydroWatershed) {
        return Number(hydroWatershed.properties['ANNUAL_RUNOFF_IN_MM'])
      }
      return null
    },
    // TODO remove isolines at future date once confirmed to be not needed
    // annualIsolineRunoff () {
    //   if (!this.watershedDetails || !this.watershedDetails.runoff_isoline_avg) {
    //     return null
    //   }
    //   return (Number(this.watershedDetails.runoff_isoline_avg)).toFixed(2)
    // },
    hydrologicalZoneModelRunoff () {
      console.log(this.watershedDetails)
      if (!this.watershedDetails || !this.watershedDetails.wally_hydro_zone_model_output_v1 ||
        !this.watershedDetails.wally_hydro_zone_model_output_v1.mean_annual_flow) {
        return null
      }
      return (Number(this.watershedDetails.wally_hydro_zone_model_output_v1.mean_annual_flow)).toFixed(2)
    },
    hydrologicalZoneModelRSquared () {
      if (!this.watershedDetails || !this.watershedDetails.wally_hydro_zone_model_output_v1 ||
        !this.watershedDetails.wally_hydro_zone_model_output_v1.r_squared) {
        return null
      }
      return (Number(this.watershedDetails.wally_hydro_zone_model_output_v1.r_squared)).toFixed(2)
    },
    showWallyModelFeatureFlag () {
      return this.app && this.app.config && this.app.config.wally_model
    }
    // TODO remove isolines at future date once confirmed to be not needed
    // isolineRunoffByMonth () {
    //   if (!this.annualIsolineRunoff) {
    //     return null
    //   }

    //   const meanAnnualDischarge = this.annualIsolineRunoff * this.watershedArea / 1000 / 365 / 24 / 60 / 60

    //   const plotData = {
    //     type: 'bar',
    //     name: 'MAD',
    //     y: this.monthlyRunoffCoefficients.map((x) => x * meanAnnualDischarge),
    //     x: months,
    //     line: { color: '#17BECF' }
    //   }

    //   const mad20 = {
    //     type: 'line',
    //     name: '20% MAD',
    //     y: Array(12).fill(0.2 * meanAnnualDischarge),
    //     x: months,
    //     line: { color: '#17BECF' }
    //   }

    //   const mad10 = {
    //     type: 'line',
    //     name: '10% MAD',
    //     y: Array(12).fill(0.1 * meanAnnualDischarge),
    //     x: months,
    //     line: { color: '#17BECF' }
    //   }

    //   return [plotData, mad20, mad10]
    // }
  },
  methods: {
  },
  mounted () {
  }
}
</script>

<style>
.titleSub {
  color: #202124;
  font-weight: bold;
  font-size: 20px;
  margin-bottom: 10px;
}
</style>
