<template>
  <div>
    <div>
      <div class="title my-5">Availability</div>
      <div v-if="annualNormalizedRunoff">
        <div>Annual normalized runoff: {{ annualNormalizedRunoff }} mm</div>
        <div>Watershed area: {{ record.properties['FEATURE_AREA_SQM'].toFixed(1) }} sq. m</div>
        <div>
          Source:
          <a href="https://catalogue.data.gov.bc.ca/dataset/hydrology-hydrometric-watershed-boundaries" target="_blank">
            Hydrometric Watersheds (DataBC)
          </a>
        </div>
        <Plotly v-if="normalizedRunoffByMonth"
          :layout="runoffLayout"
          :data="normalizedRunoffByMonth"
        ></Plotly>
      </div>
      <div v-if="annualIsolineRunoff">
        <div>Average annual runoff (by isolines): {{ annualIsolineRunoff }} mm</div>
        <div>Watershed area: {{ record.properties['area'].toFixed(2) }} sq. m</div>
        <div>
          Source:
          <a href="https://catalogue.data.gov.bc.ca/dataset/hydrology-normal-annual-runoff-isolines-1961-1990-historical" target="_blank">
            Hydrology: Normal Annual Runoff Isolines (1961 - 1990) - Historical (DataBC)
          </a>
        </div>
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
import { Plotly } from 'vue-plotly'

export default {
  name: 'WatershedAvailability',
  components: {
    Plotly
  },
  props: {
    watershedID: null,
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
      xaxis: {
        tickformat: '%B'
      },
      yaxis: {
        title: 'm3/s'
      }
    },
    isolineRunoffLayout: {
      title: 'Monthly discharge (using 1961 - 1990 runoff isolines) (m3/s)',
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
    watershedArea () {
      if (!this.record || !this.record.properties['area']) {
        return null
      }
      return Number(this.record.properties['area'])
    },
    normalizedRunoffByMonth () {
      if (!this.annualNormalizedRunoff || !this.watershedArea) {
        return null
      }

      const plotData = {
        type: 'bar',
        name: 'Runoff (Normalized Hydrometric)',
        y: this.monthlyRunoffCoefficients.map((x) => x * this.annualNormalizedRunoff * this.watershedArea / 1000 / 365 / 24 / 60 / 60),
        x: [
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
        ],
        line: { color: '#17BECF' }
      }
      return [plotData]
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
      if (!this.record || !this.record.properties['runoff_isoline_avg']) {
        return null
      }
      return (Number(this.record.properties['runoff_isoline_avg'])).toFixed(2)
    },
    isolineRunoffByMonth () {
      if (!this.annualIsolineRunoff) {
        return null
      }
      const plotData = {
        type: 'bar',
        name: 'Estimated runoff (using 1961 - 1990 runoff isolines)',
        y: this.monthlyRunoffCoefficients.map((x) => x * this.annualIsolineRunoff * this.watershedArea / 1000 / 365 / 24 / 60 / 60),
        x: [
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
        ],
        line: { color: '#17BECF' }
      }
      return [plotData]
    }
  },
  methods: {
  },
  mounted () {
  }
}
</script>

<style>

</style>
