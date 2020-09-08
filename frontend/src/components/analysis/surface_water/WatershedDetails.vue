<template>
  <v-card flat>
    <v-card-text>
      <v-row>
        <v-alert tile color="" dense class="ma-3" width="100%" text
          v-if="modelOutputs && modelOutputs.sourceDescription">
          {{ modelOutputs.sourceDescription }}
        </v-alert>
        <ModelExplanations/>
      </v-row>

      <v-row>
        <v-col>
          <v-card flat outlined tile>
            <v-card-title>
              Drainage area
              <Dialog v-bind="wmd.drainageArea"/>
            </v-card-title>
            <v-card-text class="info-blue">
              <span v-if="watershedDetails.drainage_area">
                {{ watershedDetails.drainage_area.toFixed(2) }}
                <strong>km²</strong>
              </span>
              <span v-else>
                {{ noValueText }}
              </span>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-card flat >
          <v-card-title>
            Mean Annual Discharge
            <Dialog v-bind="wmd.meanAnnualDischarge"/>
          </v-card-title>
          <v-card-text class="info-blue">
            <span v-if="modelOutputs.mad">
              {{ modelOutputs.mad }}
              <strong>m³/s</strong>
            </span>
            <span v-else>
              {{ noValueText }}
            </span>
          </v-card-text>
        </v-card>
        <v-divider vertical></v-divider>
        <v-card flat >
          <v-card-title>
            Total Annual Quantity
            <Dialog v-bind="wmd.totalAnnualQuantity"/>
          </v-card-title>
          <v-card-text class="info-blue">
            <span v-if="availabilityPlotData">
              {{ this.availabilityPlotData.reduce((a, b) => a + b, 0)
                                          .toLocaleString('en', {maximumFractionDigits: 0}) }}
              <strong>m³</strong>
            </span>
            <span v-else>
              {{ noValueText }}
            </span>
          </v-card-text>
        </v-card>
      </v-row>
      <v-divider></v-divider>
      <v-row>
        <v-card flat >
          <v-card-title>
            Mean Annual Runoff
            <Dialog v-bind="wmd.meanAnnualRunoff"/>
          </v-card-title>
          <v-card-text class="info-blue">
            <span v-if="modelOutputs.mar">
              {{ modelOutputs.mar }}
              <strong>
                l/s/km²
              </strong>
            </span>
            <span v-else>{{ noValueText }}</span>
          </v-card-text>
        </v-card>
        <v-divider vertical></v-divider>
        <v-card flat >
          <v-card-title>
            Low7Q2
            <Dialog v-bind="wmd.low7Q2"/>
          </v-card-title>
          <v-card-text class="info-blue">
            <span v-if="modelOutputs.low7q2">
              {{ modelOutputs.low7q2 }}
              <strong>m³</strong>
            </span>
            <span v-else>{{ noValueText }}</span>
          </v-card-text>
        </v-card>
        <v-divider vertical></v-divider>

        <v-card flat >
          <v-card-title>
            Dry7Q10
            <Dialog v-bind="wmd.dry7Q10"/>
          </v-card-title>
          <v-card-text class="info-blue">
            <span v-if="modelOutputs.dry7q10">
              {{ modelOutputs.dry7q10 }}
              <strong>m³/s</strong>
            </span>
            <span v-else>{{ noValueText }}</span>
          </v-card-text>
        </v-card>
      </v-row>
      <v-divider></v-divider>
      <v-row>
        <v-card flat >
          <v-card-title>
            Annual Precipitation
            <Dialog v-bind="wmd.annualPrecipitation"/>
          </v-card-title>
          <v-card-text class="info-blue">
            <span v-if="watershedDetails.annual_precipitation">
              {{ watershedDetails.annual_precipitation.toFixed(0) }}
              <strong>mm</strong>
            </span>
            <span v-else>{{ noValueText }}</span>
          </v-card-text>
        </v-card>
        <v-divider vertical></v-divider>
        <v-card flat >
          <v-card-title>
            Glacial Coverage
            <Dialog v-bind="wmd.glacialCoverage"/>
          </v-card-title>
          <v-card-text class="info-blue">
            <span v-if="watershedDetails.glacial_coverage">
              {{ watershedDetails.glacial_coverage.toFixed(2) }}
            </span>
            <span v-else>{{ noValueText }}</span>
          </v-card-text>
        </v-card>
        <v-divider vertical></v-divider>

        <v-card flat >
          <v-card-title>
            Median Elevation
            <Dialog v-bind="wmd.medianElevation"/>
          </v-card-title>
          <v-card-text class="info-blue">
            <span v-if="watershedDetails.median_elevation">
              {{ watershedDetails.median_elevation.toFixed(0) }}
              <strong>mASL</strong>
            </span>
            <span v-else>{{ noValueText }}</span>
          </v-card-text>
        </v-card>
      </v-row>
    </v-card-text>
  </v-card>
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
  name: 'WatershedDetails',
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
      var discharge = []
      var volume = []
      var percent = []
      var hoverText = []
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
    }
  },
  mounted () {
  },
  beforeDestroy () {
  }
}
</script>
