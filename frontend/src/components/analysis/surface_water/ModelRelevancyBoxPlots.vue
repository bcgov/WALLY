<template>
  <v-card :elevation="0" v-if="stats.length > 0" class="charts">
    <v-card-subtitle>Model Relevancy</v-card-subtitle>
      <div v-for="(stat, i) in stats" v-bind:key="`stat${i}`">
        <Plotly :id="`bxplt-${stat.name}`" :data="parseStat(stat)" :layout="defaultLayout" class="chart"></Plotly>
      </div>
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
    defaultLayout: {
      font: {
        family: 'BCSans, Noto Sans, Verdana, Arial'
      },
      yaxis: {
        fixedrange: true
      },
      xaxis: {
        fixedrange: true
      },
      autosize: true,
      margin: { // Margins for the chart without a title
        l: 50,
        r: 50,
        b: 50,
        t: 10,
        pad: 4
      }
    }
  }),
  methods: {
    parseStat (stat) {
      var input = this.inputs[stat.name]
      return [{
        type: 'box',
        name: stat.name,
        y: [stat.minimum, stat.quartile_1, stat.median, stat.median, stat.quartile_3, stat.maximum]
      },
      {
        type: 'line',
        name: 'Watershed Input',
        y: [input, input],
        x: [0, 1],
        line: { color: '#17BECF' }
      }]
    }
  }
  // watch: {
  //   inputs (value) {
  //     this.populateBoxPlotData()
  //   }
  // },
  // mounted () {
  //   this.populateBoxPlotData()
  // }
}
</script>
