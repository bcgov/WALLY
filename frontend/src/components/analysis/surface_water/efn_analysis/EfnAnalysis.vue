<template>
  <v-container>
    <div v-if="!modelOutputs || !licenceOutputs">
      <div>Estimating EFN...</div>
      <v-progress-linear indeterminate show></v-progress-linear>
    </div>
    <v-row v-else>
      <v-card class="watershedInfo" flat>
        <v-card-title class="title mt-5 ml-3 mr-3 pa-1 mb-2" dark>
          EFN Risk Assessment
        </v-card-title>
        <v-card-text>

          <!-- Instructions -->
          <v-col cols="12" md="12">
            <v-expansion-panels>
              <v-expansion-panel>
                <v-expansion-panel-header>
                  Instructions, and Methodology
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <v-card flat>
                    <v-card-text>
                      <EfnAnalysisInstructions />
                    </v-card-text>
                  </v-card>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-col>

          <v-card-text class="pb-0">
            <h3>Flow Levels</h3>
          </v-card-text>
          <v-card-text class="info-blue">
            <span><strong>MAD:</strong></span>
            <span v-if="modelOutputs.mad">
              {{ modelOutputs.mad }}
              m³/s
            </span>
            <span class='pl-10'><strong>MAR:</strong></span>
            <span v-if="modelOutputs.mar">
              {{ modelOutputs.mar }}
              l/s/km^2
            </span>
          </v-card-text>

          <v-card-text class="pb-0">
            <h3>Stream Size Classification: </h3>
            <p>{{ modelOutputs.mad > 10 ? 'Medium-Large (greater than 10 m3/sec MAD)' : 'Small (less than 10 m3/sec MAD)' }}</p>
          </v-card-text>

          <!-- Species Sensitivity -->
          <v-card-text class="pb-0">
            <h3>Species Sensitivity</h3>
          </v-card-text>

          <v-sheet>
            <v-row>
            <v-col cols="6" md="6">
              <v-switch
                class="px-5"
                v-model="highSensitivitySpecies"
                inset
                color="blue"
                label="Highly sensitive species in area"
              ></v-switch>
            </v-col>
            <v-col cols="6" md="6">
              <v-switch
                class="px-5"
                v-model="fishBearing"
                inset
                color="blue"
                label="Fish bearing watershed"
              ></v-switch>
              </v-col>
            </v-row>
          </v-sheet>
          <div v-if="highSensitivitySpecies">
            <EfnAnalysisSpeciesSensitivity />
          </div>
          <div v-else-if="!dataReady">
            <v-progress-linear indeterminate show></v-progress-linear>
          </div>
          <div v-else>
            <EfnAnalysisRiskTable :waterFlowData="modelOutputs" :fishBearing="fishBearing" :licenceWithdrawalData="licenceOutputs"/>
          </div>
        </v-card-text>
      </v-card>
    </v-row>
  </v-container>
</template>
<script>
import EfnAnalysisInstructions from './EfnAnalysisInstructions'
import EfnAnalysisSpeciesSensitivity from './EfnAnalysisSpeciesSensitivity'
import EfnAnalysisRiskTable from './EfnAnalysisRiskTable'
import { mapGetters } from 'vuex'
import { secondsInMonth } from '../../../../constants/months'

export default {
  name: 'EfnAnalysis',
  components: {
    EfnAnalysisInstructions,
    EfnAnalysisSpeciesSensitivity,
    EfnAnalysisRiskTable
  },
  props: [],
  data: () => ({
    fishBearing: true,
    highSensitivitySpecies: false
  }),
  computed: {
    ...mapGetters('surfaceWater', ['watershedDetails', 'licencePlotData', 'shortTermLicencePlotData']),
    dataReady () {
      return (
        this.watershedDetails &&
        this.watershedDetails.scsb2016_model &&
        !this.watershedDetails.scsb2016_model.error &&
        this.licencePlotData && this.shortTermLicencePlotData
      )
    },
    modelOutputs () {
      if (
        this.watershedDetails &&
        this.watershedDetails.scsb2016_model &&
        !this.watershedDetails.scsb2016_model.error
      ) {
        const outputs = this.watershedDetails.scsb2016_model
        const mar = outputs.find((x) => x.output_type === 'MAR')
        const mad = outputs.find((x) => x.output_type === 'MAD' && x.month === 0)
        const meanMonthlyDischarges = outputs.filter((x) => x.output_type === 'MAD' && x.month !== 0)
        return {
          mar: mar.model_result.toFixed(2),
          mad: mad.model_result.toFixed(2),
          mmd: meanMonthlyDischarges.map(m => m.model_result)
        }
      } else {
        return {
          mar: null,
          mad: null,
          mmd: null
        }
      }
    },
    licenceOutputs () {
      if (!this.licencePlotData || !this.shortTermLicencePlotData) {
        return {
          longTerm: [],
          shortTerm: []
        }
      }
      // convert m3 to m3/sec for risk analysis
      return {
        longTerm: this.licencePlotData.map((d, idx) => { return d / secondsInMonth(idx + 1) }),
        shortTerm: this.shortTermLicencePlotData.map((d, idx) => { return d / secondsInMonth(idx + 1) })
      }
    }
  },
  methods: {},
  mounted () {}
}
</script>

<style>
.v-input--switch label {
  width: 300px
}
</style>
