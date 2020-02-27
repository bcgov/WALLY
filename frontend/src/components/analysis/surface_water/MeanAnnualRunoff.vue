<template>
  <div>
    <v-btn small v-on:click="downloadWatershedInfo()" color="blue-grey lighten-4" class="mb-1 mt-5 mr-5">
      <span class="hidden-sm-and-down"><v-icon color="secondary" class="mr-1" size="18">archive</v-icon>Download Watershed Info</span>
    </v-btn>
  <div id="watershedInfo">

    <!-- <v-row v-if="watershedLoading">
      <v-col>
        <div class="headerPad titleSub">Calculating Watershed Details</div>
        <v-progress-linear show indeterminate></v-progress-linear>
      </v-col>
    </v-row> -->
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
          <!-- <div class="titleBlock">Watershed Details</div> -->
          <v-row class="borderBlock">
            <v-col>
              <div class="titleBlock">Watershed</div>
              <div class="infoBlock">
                {{watershedName}}
              </div>
            </v-col>
          </v-row>
        </v-col>

        <v-col cols=5>
          <v-row class="borderBlock">
            <v-col>
              <div class="titleBlock">Drainage Area</div>
              <div class="infoBlock">
                {{ watershedDetails.drainage_area ? watershedDetails.drainage_area : 'N/A' }}
              </div>
              <div class="unitBlock">
                km^2
              </div>
            </v-col>
          </v-row>
        </v-col>
        <!-- <v-col cols=6>
          <div class="titleExp">Watershed Name</div>
          <div class="unitExp">{{this.record ? this.record.properties.GNIS_NAME_1 : ''}}</div>
          <div class="titleExp">Average Slope</div>
          <div class="unitExp">{{modelInputs.average_slope}}</div>
          <div class="titleExp">Solar Exposure</div>
          <div class="unitExp">{{modelInputs.solar_exposure}}</div>
          <div class="titleExp">Evapo-Transpiration</div>
          <div class="unitExp">{{modelInputs.evapo_transpiration}}</div>
        </v-col> -->
      </v-row>

      <v-row class="borderSub">
        <v-col cols=4 class="colSub">
            <v-tooltip top>
              <template v-slot:activator="{ on }">
                <v-icon size="28" class="float-right" v-on="on">
                  mdi-information-outline
                </v-icon>
              </template>
              <span>Average annual precipitation in mm.</span>
            </v-tooltip>
            <div class="titleSub">Annual Precipitation</div>
          <div class="infoSub">
            {{ watershedDetails.annual_precipitation ? watershedDetails.annual_precipitation : 'N/A' }}
          </div>
          <div class="unitSub">
            mm
          </div>
        </v-col>
        <v-col cols=4 class="colSub colSubInner">
          <v-tooltip top>
            <template v-slot:activator="{ on }">
              <v-icon size="28" class="float-right" v-on="on">
                mdi-information-outline
              </v-icon>
            </template>
            <span>Percentage glacial coverage over the selected watershed area.</span>
          </v-tooltip>
          <div class="titleSub">Glacial Coverage</div>
          <div class="infoSub">
            {{ watershedDetails.glacial_coverage ? watershedDetails.glacial_coverage : 'N/A' }}
          </div>
          <div class="unitSub">
            %
          </div>
        </v-col>
        <v-col cols=4 class="colSub colSubInner">
          <v-tooltip top>
            <template v-slot:activator="{ on }">
              <v-icon size="28" class="float-right" v-on="on">
                mdi-information-outline
              </v-icon>
            </template>
            <span>Median elevation over the area of the watershed.</span>
          </v-tooltip>
          <div class="titleSub">Median Elevation</div>
          <div class="infoSub">
            {{ watershedDetails.median_elevation ? watershedDetails.median_elevation : 'N/A' }}
          </div>
          <div class="unitSub">
            mASL
          </div>
        </v-col>
      </v-row>

      <v-row class="borderBlock">
        <v-col cols=6>
          <div class="titleBlock">Mean Annual Discharge</div>
          <div class="infoBlock">
            {{ modelOutputs.mad }}
          </div>
          <div class="unitBlock">
            m^3/s
          </div>
        </v-col>
        <v-col cols=6>
          <div class="titleExp">Source</div>
          <div class="unitExp">
            The CDEM stems from the existing Canadian Digital Elevation Data (CDED). The latter were extracted
            from the hypsograph
          </div>
          <div class="titleExp">Model</div>
          <div class="unitExp">
            We used a model based upon South Coast Stewardship Baseline (Brem, Fraser Valley South, Toba, Upper Lillooet) <a
            href="https://apps.nrs.gov.bc.ca/gwells/"
            target="_blank"
            >Source Paper</a>.
          </div>
        </v-col>
      </v-row>

      <v-row class="borderSub">
        <v-col cols=4 class="colSub">
            <v-tooltip top>
              <template v-slot:activator="{ on }">
                <v-icon size="28" class="float-right" v-on="on">
                  mdi-information-outline
                </v-icon>
              </template>
              <span>This the area unit value describing annual runoff.</span>
            </v-tooltip>
            <div class="titleSub">Mean Annual Runoff</div>
          <div class="infoSub">
            {{ modelOutputs.mar }}
          </div>
          <div class="unitSub">
            l/s/km^2
          </div>
        </v-col>
        <v-col cols=4 class="colSub colSubInner">
          <v-tooltip top>
            <template v-slot:activator="{ on }">
              <v-icon size="28" class="float-right" v-on="on">
                mdi-information-outline
              </v-icon>
            </template>
            <span>2-year annual 7-day low flow.</span>
          </v-tooltip>
          <div class="titleSub">Low7Q2</div>
          <div class="infoSub">
            {{ modelOutputs.low7q2 ? modelOutputs.low7q2 : 'N/A' }}
          </div>
          <div class="unitSub">
            m^3
          </div>
        </v-col>
        <v-col cols=4 class="colSub colSubInner">
          <v-tooltip top>
            <template v-slot:activator="{ on }">
              <v-icon size="28" class="float-right" v-on="on">
                mdi-information-outline
              </v-icon>
            </template>
            <span>10-year dry return period 7-day late summer (Jun-Sep) low flow.</span>
          </v-tooltip>
          <div class="titleSub">Dry7Q10</div>
          <div class="infoSub">
            {{ modelOutputs.dry7q10 ? modelOutputs.dry7q10 : 'N/A' }}
          </div>
          <div class="unitSub">
            m^3/s
          </div>
        </v-col>
      </v-row>

        <div class="borderBlock">
          <div class="titleSub">Monthly Discharge</div>
          <div class="unitSub">
            m^3/s
          </div>
          <v-data-table
            :items="getReverseMontlyDischargeItems"
            :headers="monthHeaders"
            :hide-default-footer="true"
          />

          <WatershedDemand ref="anchor-demand" :watershedID="watershedID" :record="record" :availability="availability"/>

          <!-- <v-data-table
            :items="getMonthlyDischargeItems"
            :headers="monthlyDischargeHeaders"
            :hide-default-footer="true"
          /> -->
          <Plotly v-if="monthlyDischargeData"
            :layout="monthlyDischargeLayout()"
            :data="monthlyDischargeData"
          ></Plotly>
        </div>

        <div class="borderBlock">
          <div class="titleSub">Monthly Distribution</div>
          <div class="unitSub">
            Annual %
          </div>
          <v-data-table
            :items="getMonthlyDistributionItems"
            :headers="monthlydistributionHeaders"
            :hide-default-footer="true"
          >
            <!-- <template v-slot:item="{ item }">
              {{ (item.model_result.toFixed(4) * 100) + '%' }}
            </template> -->
          </v-data-table>
          <Plotly v-if="monthlyDistributionsData"
            :layout="monthlyDistributionsLayout()"
            :data="monthlyDistributionsData"
          ></Plotly>
        </div>

      </div>
      </div>
      </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { Plotly } from 'vue-plotly'
import moment from 'moment'
import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'
import WatershedDemand from './WatershedDemand'

export default {
  name: 'MeanAnnualRunoff',
  components: {
    Plotly,
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
      { text: 'Monthly Discharge m^3', value: 'model_result' }
    ],
    months: { 1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31 },
    secondsInMonth: 86400,
    secondsInYear: 31536000,
    monthHeaders: [
      { text: 'Unit', value: 'unit' },
      { text: 'Jan', value: 'm1' },
      { text: 'Feb', value: 'm2' },
      { text: 'Mar', value: 'm3' },
      { text: 'Apr', value: 'm4' },
      { text: 'May', value: 'm5' },
      { text: 'Jun', value: 'm6' },
      { text: 'Jul', value: 'm7' },
      { text: 'Aug', value: 'm8' },
      { text: 'Sep', value: 'm9' },
      { text: 'Oct', value: 'm10' },
      { text: 'Nov', value: 'm11' },
      { text: 'Dec', value: 'm12' }
    ]
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
          : props.WATERSHED_FEATURE_ID ? props.WATERSHED_FEATURE_ID
            : props.OBJECTID

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
      const plotData = {
        type: 'bar',
        name: 'Monthly Discharge',
        y: this.modelOutputs.monthlyDischarges.map(m => { return m.model_result }),
        x: this.monthHeaders.map((h) => h.text),
        hovertemplate: '%{y:.2f} m^3/s'
      }
      return [plotData]
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
    // getMonthlyDischargeItems () {
    //   return this.modelOutputs.monthlyDistributions.map(m => { return { month: moment.months(m.month - 1), model_result: (m.model_result * this.modelOutputs.mad.model_result).toFixed(4) } })
    // },
    getReverseMontlyDischargeItems () {
      let mds = this.modelOutputs.monthlyDischarges
      let rate = { 'unit': 'm^3/s' }
      let volume = { 'unit': 'm^3' }
      let percent = { 'unit': '%MAD' }
      for (let i = 0; i < mds.length; i++) {
        rate['m' + (i + 1)] = (mds[i].model_result).toFixed(2)
        volume['m' + (i + 1)] = (mds[i].model_result * this.months[i + 1] * this.secondsInMonth).toFixed(0)
        percent['m' + (i + 1)] = (mds[i].model_result / Number(this.modelOutputs.mad) * 100).toFixed(3)
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
      if(details && details.scsb2016_model) {
        let outputs = details.scsb2016_model
        let mar = outputs.find((x) => x.output_type === 'MAR')
        let mad = outputs.find((x) => x.output_type === 'MAD' && x.month === 0)
        let low7q2 = outputs.find((x) => x.output_type === '7Q2')
        let dry7q10 = outputs.find((x) => x.output_type === 'S-7Q10')
        let monthlyDistributions = outputs.filter((x) => x.output_type === 'MD')
        let monthlyDischarges = outputs.filter((x) => x.output_type === 'MAD' && x.month !== 0)
        this.modelOutputs = {
          mar: mar.model_result.toFixed(2),
          mad: mad.model_result.toFixed(2),
          low7q2: low7q2.model_result.toFixed(2),
          dry7q10: dry7q10.model_result.toFixed(2),
          monthlyDistributions: monthlyDistributions,
          monthlyDischarges: monthlyDischarges
        }
        this.watershedDetails = {
          median_elevation: details.median_elevation.toFixed(2),
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
          annual_precipitation: this.annualNormalizedRunoff,
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
        title: 'Monthly Discharge',
        xaxis: {
          tickformat: '%B',
          title: {
            text: 'Month',
            standoff: 20
          }
        },
        yaxis: {
          title: {
            text: 'm^3/s',
            standoff: 20
          }
        }
      }
    },
    downloadWatershedInfo (plotType) {
      // var elementHandler = {
      //   '#ignorePDF': function (element, renderer) {
      //     return true
      //   }
      // }
      let doc = jsPDF('p', 'in', [230, 900])
      let width = doc.internal.pageSize.getWidth()
      let height = doc.internal.pageSize.getHeight()
      let filename = 'watershed--'.concat(this.watershedName) + '--'.concat(new Date().toISOString()) + '.pdf'
      // doc.fromHTML(document.getElementById("watershedInfo"), 15, 0.5, { 'width': 180, 'elementHandlers': elementHandler})
      // doc.save(filename)
      html2canvas(document.getElementById('watershedInfo')).then(canvas => {
        let img = canvas.toDataURL('image/png')
        const imgProps = doc.getImageProperties(img)
        let size = this.scaleImageToFit(width, height, imgProps.width, imgProps.height)
        doc.addImage(img, 'PNG', 0, 0, size[0], size[1])
        doc.save(filename)
      })
    },
    scaleImageToFit (ws, hs, wi, hi) {
      let ri = wi / hi
      let rs = ws / hs
      let size = rs > ri ? [wi * hs / hi, hs] : [ws, hi * ws / wi]
      return size
    }

  },
  mounted () {
    // this.fetchModelData()
  },
  beforeDestroy () {
  }
}
</script>

<style>
.borderBlock {
  padding: 36px 54px 54px 50px;
}
.titleBlock {
  color: #202124;
  font-weight: bold;
  font-size: 26px;
}
.infoBlock {
  color: #1A5A96;
  font-weight: bold;
  font-size: 56px;
}
.unitBlock {
  color: #5f6368;
  font-weight: bold;
  font-size: 16px;
  margin-left: 5px;
}
.borderSub {
  border: 1px solid #dadce0;
  padding: 36px 36px 42px 36px;
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
  font-size: 20px;
}
.infoSub {
  color: #1A5A96;
  font-weight: bold;
  font-size: 44px;
}
.iconSub {
  float: right;
  font-size: 30px;
}
.unitSub {
  color: #5f6368;
  font-weight: bold;
  font-size: 16px;
  margin-left: 5px;
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
