<template>
  <div>

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
              <div class="infoBlock text-capitalize">
                {{watershedName.toLowerCase()}}
              </div>
            </v-col>
          </v-row>
        </v-col>

        <v-col cols=5>
          <v-row class="borderBlock">
            <v-col>
              <Dialog v-bind="wmd.drainageArea"/>
              <div class="titleBlock">Drainage Area</div>
              <div class="infoBlock">
                {{ watershedDetails.drainage_area ? watershedDetails.drainage_area : 'N/A' }}
              </div>
              <div class="unitBlock">
                km²
              </div>
            </v-col>
          </v-row>
        </v-col>
      </v-row>

      <v-row class="borderSub">
        <v-col cols=4 class="colSub">
          <Dialog v-bind="wmd.annualPrecipitation"/>
          <div class="titleSub">Annual Precipitation</div>
          <div class="infoSub">
            {{ watershedDetails.annual_precipitation ? watershedDetails.annual_precipitation : 'N/A' }}
          </div>
          <div class="unitSub">
            mm
          </div>
        </v-col>
        <v-col cols=4 class="colSub colSubInner">
          <Dialog v-bind="wmd.glacialCoverage"/>
          <div class="titleSub">Glacial Coverage</div>
          <div class="infoSub">
            {{ watershedDetails.glacial_coverage ? watershedDetails.glacial_coverage : 'N/A' }}
          </div>
          <div class="unitSub">
            %
          </div>
        </v-col>
        <v-col cols=4 class="colSubInner">
          <Dialog v-bind="wmd.medianElevation"/>
          <div class="titleSub">Median Elevation</div>
          <div class="infoSub">
            {{ watershedDetails.median_elevation ? watershedDetails.median_elevation : 'N/A' }}
          </div>
          <div class="unitSub">
            mASL
          </div>
        </v-col>
      </v-row>

      <div class="modelOutputBorder mt-5">
        <v-row class="borderBlock">
          <v-col cols=6>
            <div class="titleBlock">Mean Annual Discharge</div>
            <div class="infoBlock">
              {{ modelOutputs.mad }}
            </div>
            <div class="unitBlock">
              m³/s
            </div>
          </v-col>
          <v-col cols=6>
            <Dialog v-bind="wmd.meanAnnualDischarge"/>
            <div class="titleExp">Source</div>
            <div class="unitExp">
              <div>{{ modelOutputs.sourceDescription }}</div>
              <div v-if="modelOutputs.sourceLink">
                <a :href="modelOutputs.sourceLink" target="_blank">{{modelOutputs.sourceLink}}</a>
              </div>
            </div>
          </v-col>
        </v-row>

        <v-row class="borderSub">
          <v-col cols=4 class="colSub">
            <Dialog v-bind="wmd.meanAnnualRunoff"/>
              <div class="titleSub">Mean Annual Runoff</div>
            <div class="infoSub">
              {{ modelOutputs.mar }}
            </div>
            <div class="unitSub">
              l/s/km²
            </div>
          </v-col>
          <v-col cols=4 class="colSub colSubInner">
            <Dialog v-bind="wmd.low7Q2"/>
            <div class="titleSub">Low7Q2</div>
            <div class="infoSub">
              {{ modelOutputs.low7q2 ? modelOutputs.low7q2 : 'N/A' }}
            </div>
            <div class="unitSub">
              m³
            </div>
          </v-col>
          <v-col cols=4 class="colSubInner">
            <Dialog v-bind="wmd.dry7Q10"/>
            <div class="titleSub">Dry7Q10</div>
            <div class="infoSub">
              {{ modelOutputs.dry7q10 ? modelOutputs.dry7q10 : 'N/A' }}
            </div>
            <div class="unitSub">
              m³/s
            </div>
          </v-col>
        </v-row>
      </div>

      <v-divider class="my-5"/>
      <Dialog v-bind="wmd.monthlyDischarge"/>
      <div class="titleSub">Watershed Monthly Discharge</div>
      <div class="unitSub">
      </div>

      <v-data-table
        :items="getReverseMontlyDischargeItems"
        :headers="unitColumnHeader.concat(monthHeaders)"
        :hide-default-footer="true"
      />
      <Plotly v-if="monthlyDischargeData"
        :layout="monthlyDischargeLayout()"
        :data="monthlyDischargeData"
      ></Plotly>

      <WatershedDemand ref="anchor-demand" :watershedID="watershedID" :record="record" :availability="availability"/>

        <!-- <div class="borderBlock">
          <Dialog v-bind="wmd.monthlyDistribution"/>
          <div class="titleSub">Monthly Distribution</div>
          <div class="unitSub">
            Annual %
          </div>
          <v-data-table
            :items="getMonthlyDistributionItems"
            :headers="monthlydistributionHeaders"
            :hide-default-footer="true"
          >
            <template v-slot:item="{ item }">
              {{ (item.model_result.toFixed(4) * 100) + '%' }}
            </template>
          </v-data-table>
          <Plotly v-if="monthlyDistributionsData"
            :layout="monthlyDistributionsLayout()"
            :data="monthlyDistributionsData"
          ></Plotly>
        </div> -->

      </div>
    </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { Plotly } from 'vue-plotly'
import moment from 'moment'

import WatershedDemand from './watershed_demand/WatershedDemand'
import Dialog from '../../common/Dialog'
import { WatershedModelDescriptions } from '../../../constants/descriptions'

export default {
  name: 'MeanAnnualRunoff',
  components: {
    Plotly,
    Dialog,
    WatershedDemand
  },
  props: ['watershedID', 'record', 'details', 'allWatersheds'],
  data: () => ({
    watershedLoading: false,
    error: null,
    availability: [],
    watershedDetails: {
      median_elevation: 0,
      average_slope: 0,
      solar_exposure: 0,
      drainage_area: 0,
      glacial_coverage: 0,
      annual_precipitation: 0,
      evapo_transpiration: 0
    },
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

      return name
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
      return [rate, volume, percent]
    },
    watershedArea () {
      if (!this.record || !this.record.properties['FEATURE_AREA_SQM']) {
        return null
      }
      return Number(this.record.properties['FEATURE_AREA_SQM']) / 1e6
    },
    annualNormalizedRunoff () {
      const hydroWatershed = this.allWatersheds.find((ws) => {
        return ws.properties['ANNUAL_RUNOFF_IN_MM']
      })
      if (hydroWatershed) {
        return Number(hydroWatershed.properties['ANNUAL_RUNOFF_IN_MM'])
      }
      return null
    },
    madSourceDescription () {
      if (this.details && this.details.scsb2016_model) {
        return ''
      }
      return ''
    },
    madModelDescription () {
      if (this.details && this.details.scsb2016_model) {
        return ''
      }
      return ''
    }
  },
  watch: {
    details: {
      immediate: true,
      handler (val, oldVal) {
        this.updateModelData(val)
      }
    }
  },
  methods: {
    updateModelData (details) {
      // MAD Model Calculations
      if (details && details.scsb2016_model && !details.scsb2016_model.error) {
        let outputs = details.scsb2016_model
        let mar = outputs.find((x) => x.output_type === 'MAR')
        let mad = outputs.find((x) => x.output_type === 'MAD' && x.month === 0)
        let low7q2 = outputs.find((x) => x.output_type === '7Q2')
        let dry7q10 = outputs.find((x) => x.output_type === 'S-7Q10')
        let monthlyDistributions = outputs.filter((x) => x.output_type === 'MD')
        let monthlyDischarges = outputs.filter((x) => x.output_type === 'MAD' && x.month !== 0)
        this.modelOutputs = {
          sourceDescription: 'Model based on South Coast Stewardship Baseline (Sentlinger, 2016).',
          mar: mar.model_result.toFixed(2),
          mad: mad.model_result.toFixed(2),
          low7q2: low7q2.model_result.toFixed(2),
          dry7q10: dry7q10.model_result.toFixed(2),
          monthlyDistributions: monthlyDistributions,
          monthlyDischarges: monthlyDischarges
        }
        this.watershedDetails = {
          median_elevation: details.median_elevation.toFixed(0),
          average_slope: details.average_slope,
          solar_exposure: details.solar_exposure,
          drainage_area: details.drainage_area.toFixed(2),
          glacial_coverage: details.glacial_coverage.toFixed(2),
          annual_precipitation: details.annual_precipitation.toFixed(0),
          evapo_transpiration: details.potential_evapotranspiration_thornthwaite
        }
        this.availability = monthlyDischarges.map((m) => { return m.model_result * this.months[m.month] * this.secondsInMonth })
        return
      }
      // ISOLine Model Calculations as backup if Stewardship model doesn't exist
      if (this.annualNormalizedRunoff && this.watershedArea) {
        const meanAnnualDischarge = this.annualNormalizedRunoff * (this.watershedArea * 1e6) / this.secondsInYear / 1000
        var discharges = []
        var distributions = []
        for (let i = 1; i < 13; i++) {
          distributions.push({
            month: i,
            model_result: 1 / 12,
            r2: 0,
            adjusted_r2: 0,
            steyx: 0
          })
          discharges.push({
            month: i,
            model_result: meanAnnualDischarge / 12,
            r2: 0,
            adjusted_r2: 0,
            steyx: 0
          })
        }
        this.modelOutputs = {
          sourceDescription: 'Model based on normalized runoff from hydrometric watersheds.',
          sourceLink: 'https://catalogue.data.gov.bc.ca/dataset/hydrology-hydrometric-watershed-boundaries',
          mar: (meanAnnualDischarge * 1000 / this.watershedArea).toFixed(2),
          mad: meanAnnualDischarge.toFixed(2),
          low7q2: null,
          dry7q10: null,
          monthlyDistributions: distributions,
          monthlyDischarges: discharges
        }
        this.watershedDetails = {
          median_elevation: null,
          average_slope: null,
          solar_exposure: null,
          drainage_area: this.watershedArea.toFixed(2),
          glacial_coverage: null,
          annual_precipitation: null,
          evapo_transpiration: null
        }
        this.availability = discharges.map((m) => { return m.model_result * this.months[m.month] * this.secondsInMonth })
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

<style>
.borderBlock {
  padding: 18px 27px 27px 25px;
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
