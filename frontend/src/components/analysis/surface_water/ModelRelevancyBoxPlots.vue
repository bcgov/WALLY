<template>
  <v-card :elevation="0" v-if="wells.length > 0" class="charts">
    <v-card-subtitle>Model Relevancy</v-card-subtitle>
    <Plotly id="bxplt-1" :data="input1Chart.data" :layout="input1Chart.layout" class="chart"></Plotly>
    <Plotly id="bxplt-2" :data="input2Chart.data" :layout="input2Chart.layout" class="chart"></Plotly>
    <Plotly id="bxplt-3" :data="input3Chart.data" :layout="input3Chart.layout" class="chart"></Plotly>
  </v-card>
</template>
<script>
const Plotly = () => import('vue-plotly').then(module => {
  return module.Plotly
})

export default {
  name: 'ModelRelevancyBoxPlots',
  components: {
    Plotly
  },
  props: ['stats', 'inputs'],
  data: () => ({
    input1Chart: {
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
    input2Chart: {
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
    input3Chart: {
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
    populateBoxPlotData () {
      let input1 = []
      let input2 = []
      let input3 = []
      this.input1Chart.data = []
      this.input2Chart.data = []
      this.input3Chart.data = []
      
      this.stats.forEach(stat => {
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
    inputs (value) {
      this.populateBoxPlotData()
    }
  },
  mounted () {
    this.populateBoxPlotData()
  }
}
</script>
