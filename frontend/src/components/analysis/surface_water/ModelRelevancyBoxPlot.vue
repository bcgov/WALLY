<template>
  <v-card :elevation="0" class="charts">
    <Plotly :id="`bxplt-${statInfo.name}`" :data="statData()" :layout="defaultLayout" class="chart"></Plotly>
  </v-card>
</template>
<script>
const Plotly = () => import('vue-plotly').then(module => {
  return module.Plotly
})

export default {
  name: 'ModelRelevancyBoxPlot',
  components: {
    Plotly
  },
  props: ['statInfo'],
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
      showlegend: false,
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
    statData () {
      const stat = this.statInfo
      const input = this.statInfo.inputValue
      return [{
        type: 'box',
        name: stat.name,
        boxpoints: false,
        y: [stat.minimum, stat.quartile_1, stat.median, stat.median, stat.quartile_3, stat.maximum]
      },
      {
        x: [stat.name],
        y: [input],
        name: 'input value',
        marker: {
          size: 15
        }
      }]
    }
  }
}
</script>
