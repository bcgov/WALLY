<template>
  <v-card flat>
    <v-card-title
      class="title mt-5 ml-3 mr-3 pa-1 mb-2"
      dark>
      Watershed Monthly Discharge
      <Dialog dark v-bind="wmd.monthlyDischarge"/>
    </v-card-title>
    <v-card-text>
      <v-data-table
        :items="getReverseMonthlyDischargeItems"
        :headers="unitColumnHeader.concat(monthHeaders)"
        :hide-default-footer="true"
      />

      <Plotly v-if="monthlyDischargeData"
              :layout="monthlyDischargeLayout()"
              :data="monthlyDischargeData"
      ></Plotly>
    </v-card-text>
  </v-card>
</template>

<script>
import moment from 'moment'
import { WatershedModelDescriptions } from '../../../constants/descriptions'
import Dialog from '../../common/Dialog'
import { months, secondsInMonth } from '../../../constants/months'

const Plotly = () => import('vue-plotly').then(module => {
  return module.Plotly
})
export default {
  name: 'WatershedMonthlyDischarge',
  components: {
    Plotly,
    Dialog
  },
  props: ['modelOutputs'],
  data: () => ({
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
        volume.push((mds[i].model_result * months[i + 1] * secondsInMonth).toFixed(0))
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
    getReverseMonthlyDischargeItems () {
      let mds = this.modelOutputs.monthlyDischarges
      let rate = { 'unit': 'm³/s' }
      let volume = { 'unit': 'm³' }
      let percent = { 'unit': '%MAD' }
      for (let i = 0; i < mds.length; i++) {
        rate['m' + (i + 1)] = (mds[i].model_result).toFixed(2)
        volume['m' + (i + 1)] = (mds[i].model_result * months[i + 1] * secondsInMonth).toFixed(0)
        percent['m' + (i + 1)] = (mds[i].model_result / Number(this.modelOutputs.mad) * 100).toFixed(2)
      }

      return [rate, percent, volume]
    }

  },
  methods: {
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
