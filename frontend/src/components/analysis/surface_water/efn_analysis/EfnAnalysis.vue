<template>
  <v-container>
    <v-row>
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
                  Instructions, Methodology, and Data Sources
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

           <v-row>
            <v-col>
              <v-card-text class="info-blue">
                <span><strong>MAD:</strong></span>
                <span v-if="modelOutputs.mad">
                  {{ modelOutputs.mad }}
                  m³/s
                </span>
              </v-card-text>
            </v-col>
            <v-col>
              <v-card-text class="info-blue">
                <span><strong>MAR:</strong></span>
                <span v-if="modelOutputs.mar">
                  {{ modelOutputs.mar }}
                  l/s/km^2
                </span>
              </v-card-text>
            </v-col>
          </v-row>

          <!-- Species Sensitivity -->
          <v-col cols="12" md="12">
            <v-card-text class="pb-0">
              <h3>Species Sensitivity</h3>
            </v-card-text>

            <v-sheet>
              <v-switch
                class="px-5"
                v-model="highSensitivitySpecies"
                inset
                color="blue"
                label="Highly sensitive species in area"
              ></v-switch>
              <v-switch
                class="px-5"
                v-model="fishBearing"
                inset
                color="blue"
                :label="`${
                  fishBearing
                    ? 'Fish bearing watershed'
                    : 'Non-fish bearing watershed'
                }`"
              ></v-switch>
              <!-- <v-switch
              v-model="switch2"
              inset
              :label="`Switch 2: ${switch2.toString()}`"
            ></v-switch> -->
            </v-sheet>
          </v-col>

          <div v-if="highSensitivitySpecies">
            <EfnAnalysisSpeciesSensitivity />
          </div>
          <div v-else-if="fishBearing">
            <!-- Availability -->
          </div>
          <div v-else>
            <EfnAnalysisMonthlyQty :meanMonthlyDischarges="modelOutputs.mmd" />
          </div>
        </v-card-text>
      </v-card>
    </v-row>
  </v-container>
</template>
<script>
// import ApiService from '../../../../services/ApiService'
import EfnAnalysisInstructions from './EfnAnalysisInstructions'
import EfnAnalysisMonthlyQty from './EfnAnalysisMonthlyQty'
import EfnAnalysisSpeciesSensitivity from './EfnAnalysisSpeciesSensitivity'
import { mapGetters } from 'vuex'
// import qs from 'querystring'

export default {
  name: 'EfnAnalysis',
  components: {
    EfnAnalysisInstructions,
    EfnAnalysisMonthlyQty,
    EfnAnalysisSpeciesSensitivity
  },
  props: [],
  data: () => ({
    efn_data: {},
    fishBearing: false,
    highSensitivitySpecies: false
  }),
  computed: {
    ...mapGetters('surfaceWater', ['watershedDetails']),
    modelOutputs () {
      if (
        this.watershedDetails &&
        this.watershedDetails.scsb2016_model &&
        !this.watershedDetails.scsb2016_model.error
      ) {
        let outputs = this.watershedDetails.scsb2016_model
        let mar = outputs.find((x) => x.output_type === 'MAR')
        let mad = outputs.find((x) => x.output_type === 'MAD' && x.month === 0)
        let meanMonthlyDischarges = outputs.filter((x) => x.output_type === 'MAD' && x.month !== 0)
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
    }
  },
  methods: {
    // fetchEfnAnalysis () {
    //   const params = {
    //     placeholder: ''
    //   }
    //   ApiService.query(`/api/v1/efn/analysis?${qs.stringify(params)}`).then(
    //     (r) => {
    //       const data = r.data
    //       this.efn_data = data.efn_data
    //     }
    //   )
    // }
  },
  mounted () {}
}
</script>

<style>
.v-input--switch label {
  width: 300px
}
</style>
