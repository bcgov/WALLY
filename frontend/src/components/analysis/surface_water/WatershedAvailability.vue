<template>
  <div>
    <div>
      <div class="titleSub">Comparitive Runoff Models</div>
      <div v-if="annualNormalizedRunoff">
        <div>
          Source:
          <a href="https://catalogue.data.gov.bc.ca/dataset/hydrology-hydrometric-watershed-boundaries" target="_blank">
            Hydrometric Watersheds (DataBC)
          </a>
        </div>
        <div>Annual normalized runoff: {{ annualNormalizedRunoff }} mm</div>
        <div>Watershed area (highlighted area): {{ record.properties['FEATURE_AREA_SQM'].toFixed(1) }} sq. m</div>
        <div>
          Using normalized runoff from: {{ annualNormalizedRunoffSource }}
        </div>
        <Plotly v-if="normalizedRunoffByMonth"
          :layout="runoffLayout"
          :data="normalizedRunoffByMonth"
        ></Plotly>
      </div>
      <div v-if="annualIsolineRunoff">
        <div>
          Source:
          <a href="https://catalogue.data.gov.bc.ca/dataset/hydrology-normal-annual-runoff-isolines-1961-1990-historical" target="_blank">
            Hydrology: Normal Annual Runoff Isolines (1961 - 1990) - Historical (DataBC)
          </a>
        </div>
        <div>Average annual runoff (by isolines): {{ annualIsolineRunoff }} mm</div>
        <div>Watershed area: {{ record.properties['FEATURE_AREA_SQM'].toFixed(2) }} sq. m</div>
        <Plotly v-if="isolineRunoffByMonth"
          :layout="isolineRunoffLayout"
          :data="isolineRunoffByMonth"
        ></Plotly>
      </div>
    </div>
    <div v-if="!annualIsolineRunoff && !annualNormalizedRunoff">No availability models available at this location.</div>
  </div>
</template>

<script>
const Plotly = () => import('vue-plotly').then(module => {
  return module.Plotly
})
const months = [
  '2020-01-01',
  '2020-02-01',
  '2020-03-01',
  '2020-04-01',
  '2020-05-01',
  '2020-06-01',
  '2020-07-01',
  '2020-08-01',
  '2020-09-01',
  '2020-10-01',
  '2020-11-01',
  '2020-12-01'
]

import { mapGetters } from 'vuex'

export default {
  name: 'WatershedAvailability',
  components: {
    Plotly
  },
  props: {
    record: null,
    allWatersheds: {
      type: Array,
      default: () => ([])
    }
  },
  data: () => ({
    monthlyRunoffCoefficients: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    runoffLayout: {
      title: 'Runoff (Normalized annual runoff * area)',
      legend: {
        xanchor: 'center',
        x: 0.5,
        y: -0.1,
        orientation: 'h'
      },
      xaxis: {
        tickformat: '%B'
      },
      yaxis: {
        title: 'm3/s'
      }
    },
    isolineRunoffLayout: {
      title: 'Monthly discharge (using 1961 - 1990 runoff isolines)',
      legend: {
        xanchor: 'center',
        x: 0.5,
        y: -0.1,
        orientation: 'h'
      },
      xaxis: {
        tickformat: '%B'
      },
      yaxis: {
        title: 'm3/s'
      }
    }
  }),
  watch: {
  },
  computed: {
    ...mapGetters('surfaceWater', ['watershedDetails']),
    watershedArea () {
      if (!this.record || !this.record.properties['FEATURE_AREA_SQM']) {
        return null
      }
      return Number(this.record.properties['FEATURE_AREA_SQM'])
    },
    normalizedRunoffByMonth () {
      if (!this.annualNormalizedRunoff || !this.watershedArea) {
        return null
      }
      const meanAnnualDischarge = this.annualNormalizedRunoff * this.watershedArea / 1000 / 365 / 24 / 60 / 60
      const plotData = {
        type: 'bar',
        name: 'MAD',
        y: this.monthlyRunoffCoefficients.map((x) => x * meanAnnualDischarge),
        x: months,
        line: { color: '#17BECF' }
      }

      const mad20 = {
        type: 'line',
        name: '20% MAD',
        y: Array(12).fill(0.2 * meanAnnualDischarge),
        x: months,
        line: { color: '#17BECF' }
      }

      const mad10 = {
        type: 'line',
        name: '10% MAD',
        y: Array(12).fill(0.1 * meanAnnualDischarge),
        x: months,
        line: { color: '#17BECF' }
      }

      return [plotData, mad20, mad10]
    },

    annualNormalizedRunoffSource () {
      const hydroWatershed = this.allWatersheds.find((ws) => {
        return ws.properties['ANNUAL_RUNOFF_IN_MM']
      })

      if (hydroWatershed) {
        return hydroWatershed.properties['SOURCE_NAME']
      }
      return null
    },

    annualNormalizedRunoff () {
      // all watersheds in the area are checked for an annual normalized runoff.
      // this value is inferred from hydrometric stations and is only available
      // for watersheds in the Hydrometric Watersheds dataset. It leads to a rough estimate
      // only.

      const hydroWatershed = this.allWatersheds.find((ws) => {
        return ws.properties['ANNUAL_RUNOFF_IN_MM']
      })

      if (hydroWatershed) {
        return Number(hydroWatershed.properties['ANNUAL_RUNOFF_IN_MM'])
      }
      return null
    },
    annualIsolineRunoff () {
      if (!this.watershedDetails || !this.watershedDetails.runoff_isoline_avg) {
        return null
      }
      return (Number(this.watershedDetails.runoff_isoline_avg)).toFixed(2)
    },
    isolineRunoffByMonth () {
      if (!this.annualIsolineRunoff) {
        return null
      }

      const meanAnnualDischarge = this.annualIsolineRunoff * this.watershedArea / 1000 / 365 / 24 / 60 / 60

      const plotData = {
        type: 'bar',
        name: 'MAD',
        y: this.monthlyRunoffCoefficients.map((x) => x * meanAnnualDischarge),
        x: months,
        line: { color: '#17BECF' }
      }

      const mad20 = {
        type: 'line',
        name: '20% MAD',
        y: Array(12).fill(0.2 * meanAnnualDischarge),
        x: months,
        line: { color: '#17BECF' }
      }

      const mad10 = {
        type: 'line',
        name: '10% MAD',
        y: Array(12).fill(0.1 * meanAnnualDischarge),
        x: months,
        line: { color: '#17BECF' }
      }

      return [plotData, mad20, mad10]
    }
  },
  methods: {
  },
  mounted () {
  }
}
</script>

<style>
.titleSub {
  color: #202124;
  font-weight: bold;
  font-size: 20px;
  margin-bottom: 10px;
}
</style>
