<template>
  <div>
    <v-row class="borderBlock">
      <v-col cols=6>
        <div class="titleBlock">Mean Annual Discharge</div>
        <div class="infoBlock">
          {{ modelOutputs.mad.toFixed(2) }} 
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
            <span>Displays the total area of the selected watershed.</span>
          </v-tooltip>
          <div class="titleSub">Drainage Area</div>
        <div class="infoSub">
          {{ modelInputs.drainageArea.toFixed(2) }} 
        </div>
        <div class="unitSub">
          km^2
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
          {{ modelData.low7q2.toFixed(2) }} 
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
          {{ modelData.dry7q10.toFixed(2) }} 
        </div>
        <div class="unitSub">
          m^3
        </div>
      </v-col>
    </v-row>
    

      <div class="my-5">
        <div class="mb-3 ml-3 titleExp">
          Monthly Discharge
          <div class="unitExp">
            m^3
          </div>
        </div>
        
        <v-data-table
          :items="modelData.monthlyDischarge"
          :headers="monthHeaders"
          :hide-default-footer="true"
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
        <div class="mb-3 ml-3 titleExp">
          Monthly Distributions
          <div class="unitExp">
            Annual %
          </div>
        </div>
        
        <v-data-table
          :items="modelData.montlyDistributions"
          :headers="monthHeaders"
          :hide-default-footer="true"
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

    <v-row class="borderBlock">
      <v-col cols=6>
        <div class="titleBlock">Mean Annual Runoff</div>
        <div class="infoBlock">
          {{ modelData.mar.toFixed(2) }} 
        </div>
        <div class="unitBlock">
          l/s/km^2
        </div>
      </v-col>
    </v-row>
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
    modelInputs: {
      medianElevation: 0,
      averageSlope: 0,
      solarExposure: 0,
      drainageArea: 0,
      glacialCoverage: 0,
      annualPrecipitation: 0,
      evapoTranspiration: 0
    },
    modelOutputs: {
      mad: 0,
      mar: 0,
      low7q2: 0,
      dry7q10: 0,
      monthlyDischarges: [],
      monthlyDistributions: []
    },
    modelData: {
      
    },
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
        y: this.modelOutputs.monthlyDistributions,
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
        type: 'scatter',
        name: 'Monthly Discharge',
        y: this.modelOutputs.monthlyDischarges,
        x: this.monthHeaders.map((h) => h.text),
        hovertemplate: '%{y:.2f} m^3/s'
      }
      return [plotData]
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
          let outputs = r.data.model_outputs
          let mar = r.data.outputs.find((x) => x.output_type === 'MAR')
          let mad = r.data.outputs.find((x) => x.output_type === 'MAD')
          let low7q2 = r.data.outputs.find((x) => x.output_type === '7Q2')
          let dry7q10 = r.data.outputs.find((x) => x.output_type === 'S-7Q10')
          let monthlyDistributions = r.data.outputs.filter((x) => x.output_type === 'MD')

          this.modelOutputs = {
            mar: mar,
            mad: mad,
            low7q2: low7q2,
            dry7q10: dry7q10,
            monthlyDistributions: monthlyDistributions
          }

          this.modelInputs = r.data.model_inputs
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
  font-size: 12px;
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
