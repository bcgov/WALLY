<template>
  <div>
    <div class="title mt-5">Mean Annual Discharge Model</div>
      
      <span>Drainage Area:</span> {{ modelData.drainageArea.toFixed(2) }} km^2
      <span>Mean annual discharge:</span> {{ modelData.mad.toFixed(2) }} m^3
      <span>Mean annual runoff:</span> {{ modelData.mar.toFixed(2) }} l/s/km^2
      <span>2-year annual 7-day low flow:</span> {{ modelData.low7q2.toFixed(2) }} m^3
      <span>10-year dry return period 7-day late summer (Jun-Sep) low flow:</span> {{ modelData.dry7q10.toFixed(2) }} m^3

      <div class="my-5">
        <div class="mb-3">Monthly Discharge</div>
        <v-data-table
          :items="modelData.monthlyDischarge"
          :headers="monthHeaders"
        >
          <template v-slot:item="{ item }">
            {{ item.toFixed(2) }}
          </template>
        </v-data-table>
        <Plotly v-if="monthlyDischargeData"
          :layout="monthlyDischargeLayout"
          :data="monthlyDischargeData"
        ></Plotly>
      </div>

      <div class="my-5">
        <div class="mb-3">Monthly Distributions</div>
        <v-data-table
          :items="modelData.montlyDistributions"
          :headers="monthHeaders"
        >
          <template v-slot:item="{ item }">
            {{ (item.toFixed(4) * 100) + '%' }}
          </template>
        </v-data-table>
        <Plotly v-if="monthlyDistributionsData"
          :layout="monthlyDistributionsLayout"
          :data="monthlyDistributionsData"
        ></Plotly>
      </div>

    </div>
</template>

<script>
import { mapGetters } from 'vuex'
import ApiService from '../../../services/ApiService'

export default {
  name: 'MeanAnnualRunoff',
  components: {
  },
  props: ['watershedID', 'record'],
  data: () => ({
    modelData: null,
    // coefficientTableHeaders: [
    //   { text: 'Output', value: 'model_output_type' },
    //   { text: 'Month', value: 'month' },
    //   { text: 'Med. Elev.', value: 'month' },
    //   { text: 'Month', value: 'month' },
    // ],
    monthHeaders: [
      { text: 'Jan', value: '1' },
      { text: 'Feb', value: '2' },
      { text: 'Mar', value: '3' },
      { text: 'Apr', value: '4' },
      { text: 'May', value: '5' },
      { text: 'Jun', value: '6' },
      { text: 'Jul', value: '7' },
      { text: 'Aug', value: '8' },
      { text: 'Sep', value: '9' },
      { text: 'Oct', value: '10' },
      { text: 'Nov', value: '11' },
      { text: 'Dec', value: '12' }
    ],
    
  }),
  computed: {
    ...mapGetters('map', ['map']),
    monthlyDistributionsData () {
      if (!this.modelData.montlyDistributions) {
        return null
      }
      const plotData = {
        type: 'scatter',
        name: 'Monthly Distributions',
        y: this.modelData.montlyDistributions,
        x: this.monthHeaders.map((h) => h.text),
        hovertemplate: '%MD: %{y:.2f}',
      }
      return [plotData]
    },
    monthlyDischargeData () {
      if (!this.modelData.monthlyDischarge) {
        return null
      }
      const plotData = {
        type: 'scatter',
        name: 'Monthly Discharge',
        y: this.modelData.monthlyDischarge,
        x: this.monthHeaders.map((h) => h.text),
        hovertemplate: '%{y:.2f} m^3/s',
      }
      return [plotData]
    },
  },
  watch: {
    watershedID () {
      this.fetchModelData()
    }
  },
  methods: {
    fetchModelData () {
      ApiService.query(`/api/v1/mad/`)
        .then(r => {
          this.licenceData = r.data
          const max = Math.max(...r.data.licences.features.map(x => Number(x.properties.qty_m3_yr)))
          this.addLicencesLayer('waterLicences', r.data.licences, '#00e676', 0.5, max)
        })
        .catch(e => {
          console.error(e)
        })
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
        title: 'Monthly Discharge',
        xaxis: {
          tickformat: '%B'
        },
        yaxis: {
          title: 'm^3/s'
        }
      }
    }

  },
  mounted () {
    this.fetchModelData()
  },
  beforeDestroy () {
  }
}
</script>

<style>

</style>
