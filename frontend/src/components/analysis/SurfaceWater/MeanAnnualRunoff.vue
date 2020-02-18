<template>
  <div>
    <v-row class="borderSub">
      <v-col cols=6>
        <div class="titleBlock">Watershed Details</div>
        <v-row class="borderBlock">
          <v-col>
            <div class="titleBlock">Drainage Area</div>
            <div class="infoBlock">
              {{ modelInputs.drainage_area.toFixed(2) }} 
            </div>
            <div class="unitBlock">
              km^2
            </div>
          </v-col>
        </v-row>
      </v-col>
      <v-col cols=6>
        <div class="titleExp">Watershed Name</div>
        <div class="unitExp">{{this.record ? this.record.name : ''}}</div>
        <!-- <div class="titleExp">Average Slope</div>
        <div class="unitExp">{{modelInputs.average_slope}}</div>
        <div class="titleExp">Solar Exposure</div>
        <div class="unitExp">{{modelInputs.solar_exposure}}</div>
        <div class="titleExp">Evapo-Transpiration</div>
        <div class="unitExp">{{modelInputs.evapo_transpiration}}</div> -->
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
            <span>Average annual precipitation in mm.</span>
          </v-tooltip>
          <div class="titleSub">Annual Precipitation</div>
        <div class="infoSub">
          {{ modelInputs.annual_precipitation.toFixed(2) }} 
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
          {{ modelInputs.glacial_coverage.toFixed(2) }} 
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
          {{ modelInputs.median_elevation.toFixed(2) }} 
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
          {{ modelOutputs.mad.model_result.toFixed(2) }} 
        </div>
        <div class="unitBlock">
          m^3
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
          {{ modelOutputs.mar.model_result.toFixed(2) }} 
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
          {{ modelOutputs.low7q2.model_result.toFixed(2) }} 
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
          {{ modelOutputs.dry7q10.model_result.toFixed(2) }} 
        </div>
        <div class="unitSub">
          m^3
        </div>
      </v-col>
    </v-row>


      <div class="borderBlock">
        <div class="titleSub">Monthly Discharge</div>
        <div class="unitSub">
          m^3
        </div>
        <v-data-table
          :items="getReverseMontlyDischargeItems"
          :headers="monthHeaders"
          :hide-default-footer="true"
        />
        <!-- <v-data-table
          :items="getMonthlyDischargeItems"
          :headers="monthlyDischargeHeaders"
          :hide-default-footer="true"
        /> -->
        <Plotly v-if="monthlyDischargeData"
          :layout="monthlyDischargeLayout"
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
          :layout="monthlyDistributionsLayout"
          :data="monthlyDistributionsData"
        ></Plotly>
      </div>

    
    </div>
</template>

<script>
import { mapGetters } from 'vuex'
import ApiService from '../../../services/ApiService'
import { Plotly } from 'vue-plotly'
import moment from 'moment'

export default {
  name: 'MeanAnnualRunoff',
  components: {
    Plotly
  },
  props: ['watershedID', 'record'],
  data: () => ({
    modelInputs: {
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
      { text: 'Steyx', value: 'steyx' },
    ],
    monthlyDischargeHeaders: [
      { text: 'Month', value: 'month' },
      { text: 'Monthly Discharge m^3', value: 'model_result' },
    ],
    monthHeaders: [
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
    monthlyDistributionsData () {
      if (!this.modelOutputs.monthlyDistributions) {
        return null
      }
      const plotData = {
        type: 'scatter',
        name: 'Monthly Distributions',
        y: this.modelOutputs.monthlyDistributions.map(m => { return m.model_result }),
        x: this.monthHeaders.map((h) => h.text),
        hovertemplate: '%MD: %{y:.2f}'
      }
      return [plotData]
    },
    monthlyDischargeData () {
      if (!this.modelOutputs.monthlyDistributions) {
        return null
      }
      const plotData = {
        type: 'scatter',
        name: 'Monthly Discharge',
        y: this.modelOutputs.monthlyDistributions.map(m => { return m.model_result * this.modelOutputs.mad.model_result }),
        x: this.monthHeaders.map((h) => h.text),
        hovertemplate: '%{y:.2f} m^3/s'
      }
      return [plotData]
    },
    getMonthlyDistributionItems () {
      return this.modelOutputs.monthlyDistributions.map(m => { return { 
        month: moment.months(m.month - 1), 
        model_result: (m.model_result * 100).toFixed(2),
        r2: m.r2,
        adjusted_r2: m.adjusted_r2,
        steyx: m.steyx
      }})
    },
    getMonthlyDischargeItems () {
      return this.modelOutputs.monthlyDistributions.map(m => { return { month: moment.months(m.month - 1), model_result: (m.model_result * this.modelOutputs.mad.model_result).toFixed(4) }})
    },
    getReverseMontlyDischargeItems () {
      let mds = this.modelOutputs.monthlyDistributions
      let obj = {}
      for (let i = 0; i < mds.length; i++) {
        obj['m'+(i+1)] = (mds[i].model_result * this.modelOutputs.mad.model_result).toFixed(2)
      }
      console.log(obj)
      return [obj]
    }
  },
  watch: {
    watershedID () {
      this.fetchModelData()
    }
  },
  methods: {
    fetchModelData () {
      ApiService.query(`/api/v1/marmodel?zone=25&polygon=[[[-123.02201370854334,50.12217755683673],[-122.9494857102976,50.11744970738056],[-122.96039700206931,50.13985145871305],[-123.02201370854334,50.12217755683673]]]`)
        .then(r => {
          if (r.data && r.data.model_outputs && r.data.model_inputs) {
            let outputs = r.data.model_outputs
            let mar = outputs.find((x) => x.output_type === 'MAR')
            let mad = outputs.find((x) => x.output_type === 'MAD')
            let low7q2 = outputs.find((x) => x.output_type === '7Q2')
            let dry7q10 = outputs.find((x) => x.output_type === 'S-7Q10')
            let monthlyDistributions = outputs.filter((x) => x.output_type === 'MD')

            this.modelOutputs = {
              mar: mar,
              mad: mad,
              low7q2: low7q2,
              dry7q10: dry7q10,
              monthlyDistributions: monthlyDistributions
            }
            this.modelInputs = r.data.model_inputs
          }
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
          tickformat: '%B',
          title: {
            text: "Month",
            standoff: 20
          }
        },
        yaxis: {
          title: {
            text: "m^3/s",
            standoff: 20
          }
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
</style>
