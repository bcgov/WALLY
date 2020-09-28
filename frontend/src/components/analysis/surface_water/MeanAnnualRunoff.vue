<template>
  <div>
    <div class="titleBlock">Watershed Details</div>
    <div class="ml-3 unitSub">
      <div>{{ modelOutputs.sourceDescription }}</div>
      <div v-if="modelOutputs.sourceLink">
        Source Link: <a :href="modelOutputs.sourceLink" target="_blank">{{modelOutputs.sourceLink}}</a>
      </div>
    </div>
    <ModelExplanations/>

    <v-btn small v-on:click="downloadWatershedInfo()" color="blue-grey lighten-4" class="mb-1 mt-5 mr-5">
      <span class="hidden-sm-and-down"><v-icon color="secondary" class="mr-1" size="18">archive</v-icon>Download Watershed Info</span>
    </v-btn>

  <div id="watershedInfo">
    <div v-if="error">
      <v-row class="borderBlock">
        <v-col>
          <div class="titleSub">Error Calculating Watershed</div>
          <div class="infoSub">
            {{error}}
          </div>
        </v-col>
      </v-row>
    </div>
    <div v-else-if="watershedDetails">

      <v-row>
        <v-col cols=7>
          <v-row class="borderBlock">
            <v-col>
              <div class="titleBlock">Watershed</div>
              <div class="infoBlock text-capitalize" v-if="watershedName">
                {{watershedName.toLowerCase()}}
              </div>
              <div class="unitSub" v-else>
                {{'No watershed name found'}}
              </div>
            </v-col>
          </v-row>
        </v-col>

        <v-col cols=5>
          <v-row class="borderBlock">
            <v-col>
              <Dialog v-bind="wmd.drainageArea"/>
              <div class="titleBlock">Drainage Area</div>
              <div v-if="watershedDetails.drainage_area">
                <div class="infoSub">
                  {{ watershedDetails.drainage_area.toFixed(2) }}
                </div>
                <div class="unitSub">km²</div>
              </div>
              <div class="unitSub" v-else>
                {{ noValueText }}
              </div>
            </v-col>
          </v-row>
        </v-col>
      </v-row>

      <div class="modelOutputBorder">
        <v-row class="borderBlock">
          <v-col cols=6 class="colSub">
            <Dialog v-bind="wmd.meanAnnualDischarge"/>
            <div class="titleBlock">Mean Annual Discharge</div>
            <div v-if="modelOutputs.mad">
              <div class="infoBlock">
                {{ modelOutputs.mad }}
              </div>
              <div class="unitBlock">m³/s</div>
            </div>
            <div class="unitSub" v-else>
              {{ noValueText }}
            </div>
          </v-col>

          <v-col cols=6 class="colSubInner">
            <Dialog v-bind="wmd.totalAnnualQuantity"/>
            <div class="titleBlock">Total Annual Quantity</div>
            <div v-if="availabilityPlotData">
              <div class="infoBlock">
                {{this.availabilityPlotData.reduce((a, b) => a + b, 0).toLocaleString('en', {maximumFractionDigits: 0})}}
              </div>
              <div class="unitBlock">m³</div>
            </div>
            <div class="unitSub" v-else>
              {{ noValueText }}
            </div>
          </v-col>
        </v-row>

        <v-row class="borderSub">
          <v-col cols=4 class="colSub">
            <Dialog v-bind="wmd.meanAnnualRunoff"/>
            <div class="titleSub">Mean Annual Runoff</div>
            <div v-if="modelOutputs.mar">
              <div class="infoSub">
                {{ modelOutputs.mar }}
              </div>
              <div class="unitSub">l/s/km²</div>
            </div>
            <div class="unitSub" v-else>
              {{ noValueText }}
            </div>
          </v-col>
          <v-col cols=4 class="colSub colSubInner">
            <Dialog v-bind="wmd.low7Q2"/>
            <div class="titleSub">Low7Q2</div>
            <div v-if="modelOutputs.low7q2">
              <div class="infoSub">
                {{ modelOutputs.low7q2 }}
              </div>
              <div class="unitSub">m³</div>
            </div>
            <div class="unitSub" v-else>
              {{ noValueText }}
            </div>
          </v-col>
          <v-col cols=4 class="colSubInner">
            <Dialog v-bind="wmd.dry7Q10"/>
            <div class="titleSub">Dry7Q10</div>
            <div v-if="modelOutputs.dry7q10">
              <div class="infoSub">
                {{ modelOutputs.dry7q10 }}
              </div>
              <div class="unitSub">m³/s</div>
            </div>
            <div class="unitSub" v-else>
              {{ noValueText }}
            </div>
          </v-col>
        </v-row>
      </div>

      <v-row class="borderSub mt-5">
        <v-col cols=4 class="colSub">
          <Dialog v-bind="wmd.annualPrecipitation"/>
          <div class="titleSub">Annual Precipitation</div>
          <div v-if="watershedDetails.annual_precipitation">
            <div class="infoSub">
              {{ watershedDetails.annual_precipitation.toFixed(0) }}
            </div>
            <div class="unitSub">mm</div>
          </div>
          <div class="unitSub" v-else>
            {{ noValueText }}
          </div>
        </v-col>
        <v-col cols=4 class="colSub colSubInner">
          <Dialog v-bind="wmd.glacialCoverage"/>
          <div class="titleSub">Glacial Coverage</div>
          <div v-if="watershedDetails.glacial_coverage">
            <div class="infoSub">
              {{ watershedDetails.glacial_coverage.toFixed(2) }}
            </div>
            <div class="unitSub">%</div>
          </div>
          <div class="unitSub" v-else>
            {{ noValueText }}
          </div>
        </v-col>
        <v-col cols=4 class="colSubInner">
          <Dialog v-bind="wmd.medianElevation"/>
          <div class="titleSub">Median Elevation</div>
          <div v-if="watershedDetails.median_elevation">
            <div class="infoSub">
              {{ watershedDetails.median_elevation.toFixed(0) }}
            </div>
            <div class="unitSub">mASL</div>
          </div>
          <div class="unitSub" v-else>
            {{ noValueText }}
          </div>
        </v-col>
      </v-row>

      <div v-if="showWallyModelFeatureFlag" class="modelOutputBorder">
        <v-row class="borderBlock">
          <v-col cols=6 class="colSub">
            <div class="titleBlock">Wally Hydro Zone Model</div>
            <div v-if="wally_model_mar">
              <div class="infoBlock">
                {{ wally_model_mar }}
              </div>
              <div class="unitBlock">m³/s</div>
            </div>
            <div class="unitSub" v-else>
              {{ noValueText }}
            </div>
          </v-col>

          <v-col cols=6 class="colSubInner">
            <Dialog v-bind="wmd.totalAnnualQuantity"/>
            <div class="titleBlock">Model R Squared</div>
            <div v-if="wally_model_r2">
              <div class="infoBlock">
                {{wally_model_r2}}
              </div>
              <div class="unitBlock">Model Fit</div>
            </div>
            <div class="unitSub" v-else>
              {{ noValueText }}
            </div>
          </v-col>
        </v-row>
      </div>

      <v-divider class="my-5"/>
      <div v-if="modelOutputs.monthlyDischarges.length > 0">
        <Dialog v-bind="wmd.monthlyDischarge"/>
        <div class="titleSub mb-8">Watershed Monthly Discharge</div>
        <v-data-table
          :items="getReverseMontlyDischargeItems"
          :headers="unitColumnHeader.concat(monthHeaders)"
          :hide-default-footer="true"
        />
        <Plotly v-if="monthlyDischargeData"
          :layout="monthlyDischargeLayout()"
          :data="monthlyDischargeData"
        ></Plotly>
      </div>

      </div>
    </div>
    </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
import moment from 'moment'

import Dialog from '../../common/Dialog'
import { WatershedModelDescriptions } from '../../../constants/descriptions'
import ModelExplanations from './ModelExplanations'

const Plotly = () => import('vue-plotly').then(module => {
  return module.Plotly
})

export default {
  name: 'MeanAnnualRunoff',
  components: {
    Plotly,
    Dialog,
    ModelExplanations
  },
  props: ['record'],
  data: () => ({
    watershedLoading: false,
    error: null,
    noValueText: 'No info available',
    modelOutputs: {
      mad: 0,
      mar: 0,
      low7q2: 0,
      dry7q10: 0,
      monthlyDischarges: [],
      monthlyDistributions: []
    },
    wally_model_mar: 0,
    wally_model_r2: 0,
    monthlydistributionHeaders: [
      { text: 'Month', value: 'month' },
      { text: 'MD(%)', value: 'model_result' },
      { text: 'R2', value: 'r2' },
      { text: 'Adjusted R2', value: 'adjusted_r2' },
      { text: 'Steyx', value: 'steyx' }
    ],
    monthlyDischargeHeaders: [
      { text: 'Month', value: 'month' },
      { text: 'Monthly Discharge m³', value: 'model_result' }
    ],
    months: { 1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31 },
    secondsInMonth: 86400,
    secondsInYear: 31536000,
    unitColumnHeader: [
      { text: 'Unit', value: 'unit' }
    ],
    monthHeaders: [
      { text: 'Jan', value: 'm1', align: 'end' },
      { text: 'Feb', value: 'm2', align: 'end' },
      { text: 'Mar', value: 'm3', align: 'end' },
      { text: 'Apr', value: 'm4', align: 'end' },
      { text: 'May', value: 'm5', align: 'end' },
      { text: 'Jun', value: 'm6', align: 'end' },
      { text: 'Jul', value: 'm7', align: 'end' },
      { text: 'Aug', value: 'm8', align: 'end' },
      { text: 'Sep', value: 'm9', align: 'end' },
      { text: 'Oct', value: 'm10', align: 'end' },
      { text: 'Nov', value: 'm11', align: 'end' },
      { text: 'Dec', value: 'm12', align: 'end' }
    ],
    wmd: WatershedModelDescriptions
  }),
  computed: {
    ...mapGetters('map', ['map']),
    ...mapGetters('surfaceWater', ['availabilityPlotData', 'watershedDetails']),
    watershedName () {
      if (!this.record) {
        return ''
      }
      let name = ''
      let props = this.record.properties
      name = props.GNIS_NAME_1 ? props.GNIS_NAME_1
        : props.SOURCE_NAME ? props.SOURCE_NAME
          : props.name ? props.name
            : props.WATERSHED_FEATURE_ID ? props.WATERSHED_FEATURE_ID
              : props.OBJECTID ? props.OBJECTID : ''
      console.log('name')
      console.log(name)
      return name.toString()
    },
    monthlyDistributionsData () {
      if (!this.modelOutputs.monthlyDistributions) {
        return null
      }
      const plotData = {
        type: 'bar',
        name: 'Monthly Distributions',
        y: this.modelOutputs.monthlyDistributions.map(m => { return m.model_result }),
        x: this.monthHeaders.map((h) => h.text),
        hovertemplate: '%MD: %{y:.2f}'
      }
      return [plotData]
    },
    monthlyDischargeData () {
      if (!this.modelOutputs.monthlyDischarges) {
        return null
      }
      let mds = this.modelOutputs.monthlyDischarges
      let discharge = []
      let volume = []
      let percent = []
      let hoverText = []
      for (let i = 0; i < mds.length; i++) {
        discharge.push((mds[i].model_result).toFixed(2))
        volume.push((mds[i].model_result * this.months[i + 1] * this.secondsInMonth).toFixed(0))
        percent.push((mds[i].model_result / Number(this.modelOutputs.mad) * 100).toFixed(2))
        hoverText.push(volume[i] + ' m³ <br>' + discharge[i] + ' m³/s <br>' + percent[i] + '% MAD')
      }
      const volumeData = {
        type: 'bar',
        name: 'Monthly Volume',
        y: volume,
        x: this.monthHeaders.map((h) => h.text),
        text: hoverText,
        hoverinfo: 'text'
      }
      return [volumeData]
    },
    getMonthlyDistributionItems () {
      return this.modelOutputs.monthlyDistributions.map(m => {
        return {
          month: moment.months(m.month - 1),
          model_result: (m.model_result * 100).toFixed(2),
          r2: m.r2,
          adjusted_r2: m.adjusted_r2,
          steyx: m.steyx
        }
      })
    },
    getReverseMontlyDischargeItems () {
      let mds = this.modelOutputs.monthlyDischarges
      let rate = { 'unit': 'm³/s' }
      let volume = { 'unit': 'm³' }
      let percent = { 'unit': '%MAD' }
      for (let i = 0; i < mds.length; i++) {
        rate['m' + (i + 1)] = (mds[i].model_result).toFixed(2)
        volume['m' + (i + 1)] = (mds[i].model_result * this.months[i + 1] * this.secondsInMonth).toFixed(0)
        percent['m' + (i + 1)] = (mds[i].model_result / Number(this.modelOutputs.mad) * 100).toFixed(2)
      }
      return [rate, percent, volume]
    },
    watershedArea () {
      if (!this.record || !this.record.properties['FEATURE_AREA_SQM']) {
        return null
      }
      return Number(this.record.properties['FEATURE_AREA_SQM']) / 1e6
    }
  },
  watch: {
    watershedDetails: {
      immediate: true,
      handler (val, oldVal) {
        this.updateModelData(val)
      }
    }
  },
  methods: {
    ...mapMutations('surfaceWater', ['setAvailabilityPlotData']),
    updateModelData (details) {
      // MAD Model Calculations
      if (!details) {
        return
      }

      if (details.wally_hydro_zone_model_output && !details.wally_hydro_zone_model_output.error) {
        this.wally_model_mar = details.wally_hydro_zone_model_output.mean_annual_flow.toFixed(2)
        this.wally_model_r2 = details.wally_hydro_zone_model_output.r_squared.toFixed(2)
      }

      if (details && details.scsb2016_model && !details.scsb2016_model.error) {
        let outputs = details.scsb2016_model
        let mar = outputs.find((x) => x.output_type === 'MAR')
        let mad = outputs.find((x) => x.output_type === 'MAD' && x.month === 0)
        let low7q2 = outputs.find((x) => x.output_type === '7Q2')
        let dry7q10 = outputs.find((x) => x.output_type === 'S-7Q10')
        let monthlyDistributions = outputs.filter((x) => x.output_type === 'MD')
        let monthlyDischarges = outputs.filter((x) => x.output_type === 'MAD' && x.month !== 0)
        this.modelOutputs = {
          sourceDescription: 'Model output based on South Coast Stewardship Baseline (Sentlinger, 2016).',
          mar: mar.model_result.toFixed(2),
          mad: mad.model_result.toFixed(2),
          low7q2: low7q2.model_result.toFixed(2),
          dry7q10: dry7q10.model_result.toFixed(2),
          monthlyDistributions: monthlyDistributions,
          monthlyDischarges: monthlyDischarges
        }
        let availability = monthlyDischarges.map((m) => { return m.model_result * this.months[m.month] * this.secondsInMonth })
        this.setAvailabilityPlotData(availability)
      } else {
        this.setAvailabilityPlotData(null)
      }
    },
    monthlyDistributionsLayout () {
      return {
        title: 'Monthly Distributions',
        xaxis: {
          tickformat: '%B'
        },
        yaxis: {
          title: '%MD'
        }
      }
    },
    monthlyDischargeLayout () {
      return {
        title: 'Monthly Discharge Values',
        xaxis: {
          tickformat: '%B',
          title: {
            text: 'Month',
            standoff: 20
          }
        }
      }
    },
    showWallyModelFeatureFlag () {
      return this.app && this.app.config && this.app.config.wally_model
    }
  },
  mounted () {
  },
  beforeDestroy () {
  }
}
</script>

<style>
.borderBlock {
  padding: 18px 27px 20px 25px;
}
.titleBlock {
  color: #202124;
  font-weight: bold;
  font-size: 26px;
}
.infoBlock {
  color: #1A5A96;
  font-weight: bold;
  font-size: 26px;
}
.unitBlock {
  color: #5f6368;
  font-weight: bold;
  font-size: 16px;
  margin-left: 5px;
}
.modelOutputBorder {
  border: 1px solid #dadce0;
}
.borderSub {
  padding: 24px 24px 28px 24px;
}
.colSub {
  border-right: 1px solid #dadce0;
}
.colSubInner {
  padding-left: 42px;
}
.titleSub {
  color: #202124;
  font-weight: bold;
  font-size: 26px;
}
.infoSub {
  color: #1A5A96;
  font-weight: bold;
  font-size: 26px;
}
.iconSub {
  float: right;
  font-size: 26px;
}
.unitSub {
  color: #5f6368;
  font-weight: bold;
  font-size: 16px;
  margin-left: 5px;
  margin-bottom: 20px;
}
.inputTitle {
  color: #202124;
  font-weight: bold;
  font-size: 18px;
}
.inputValueText {
  color: #1A5A96;
  font-weight: bold;
  font-size: 18px;
}

.titleExp {
  color: #202124;
  font-weight: 600;
  font-size: 18px;
}
.unitExp {
  color: #202124;
  font-weight: 500;
  font-size: 16px;
  margin-bottom: 10px;
}
.chartTitle {
  color: #202124;
  font-weight: 600;
  font-size: 18px;
  border-bottom: 1px solid #dadce0;
}
.headerPad {
  padding: 36px 54px 38px 50px;
}
</style>
