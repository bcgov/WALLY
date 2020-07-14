<template>
  <v-card :elevation="0" v-if="wells.length > 0" class="charts">
    <v-card-subtitle>Insights ({{wells.length}} wells)</v-card-subtitle>
    <Plotly id="boxPlotYield" :data="boxPlotYieldData.data" :layout="boxPlotYieldData.layout" class="chart"></Plotly>
    <Plotly id="boxPlotFinishedDepth" :data="boxPlotFinishedDepthData.data" :layout="boxPlotFinishedDepthData.layout" class="chart"></Plotly>
    <Plotly id="boxPlotSWL" :data="boxPlotSWLData.data" :layout="boxPlotSWLData.layout" class="chart"></Plotly>
  </v-card>
</template>
<script>
const Plotly = () => import('vue-plotly').then(module => {
  return module.Plotly
})

export default {
  name: 'WellsNearbyBoxPlot',
  components: {
    Plotly
  },
  props: ['wells'],
  data: () => ({
    boxPlotSWLData: {
      data: [],
      layout: {
        font: {
          family: 'BCSans, Noto Sans, Verdana, Arial'
        },
        yaxis: {
          autorange: 'reversed',
          fixedrange: true
        },
        xaxis: {
          fixedrange: true
        },
        autosize: false,
        width: 250,
        margin: { // Margins for the chart without a title
          l: 50,
          r: 50,
          b: 50,
          t: 10,
          pad: 4
        }
      }
    },
    boxPlotYieldData: {
      data: [],
      layout: {
        font: {
          family: 'BCSans, Noto Sans, Verdana, Arial'
        },
        yaxis: {
          autorange: 'reversed',
          fixedrange: true
        },
        xaxis: {
          fixedrange: true
        },
        autosize: false,
        width: 250,
        margin: { // Margins for the chart without a title
          l: 50,
          r: 50,
          b: 50,
          t: 10,
          pad: 4
        }
      }
    },
    boxPlotFinishedDepthData: {
      data: [],
      layout: {
        font: {
          family: 'BCSans, Noto Sans, Verdana, Arial'
        },
        yaxis: {
          autorange: 'reversed',
          fixedrange: true
        },
        xaxis: {
          fixedrange: true
        },
        autosize: false,
        width: 250,
        margin: { // Margins for the chart without a title
          l: 50,
          r: 50,
          b: 50,
          t: 10,
          pad: 4
        }
      }
    }
  }),
  methods: {
    populateBoxPlotData (wells) {
      let yieldY = []
      let depthY = []
      let swlY = []

      this.boxPlotSWLData.data = []
      this.boxPlotYieldData.data = []
      this.boxPlotFinishedDepthData.data = []
      wells.forEach(well => {
        yieldY.push(Number(well.well_yield))
        depthY.push(Number(well.finished_well_depth))
        swlY.push(Number(well.static_water_level))
      })
      this.boxPlotYieldData.data.push({
        y: yieldY,
        type: 'box',
        name: 'Well Yields (USGPM)'
      })
      this.boxPlotFinishedDepthData.data.push({
        y: depthY,
        type: 'box',
        name: 'Finished Well Depth (ft bgl)'
      })
      this.boxPlotSWLData.data.push({
        y: swlY,
        type: 'box',
        name: 'Static Water Level Depth (ft)'
      })
    }
  },
  watch: {
    wells (value) {
      this.populateBoxPlotData(value)
    }
  },
  mounted () {
    this.populateBoxPlotData(this.wells)
  }
}
</script>
