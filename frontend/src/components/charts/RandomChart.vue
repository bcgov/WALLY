<template>
  <div class="small">
    <line-chart :chart-data="datacollection.line"></line-chart>
<!--    <doughnut-chart :chart-data="datacollection.doughnut"></doughnut-chart>-->
    <button @click="fillData()">Randomize</button>
  </div>
</template>

<script>
  import LineChart from './LineChart.js'
  import DoughnutChart from './DoughnutChart.js'

  export default {
    components: {
      LineChart,
      DoughnutChart
    },
    data () {
      return {
        datacollection: { line: null, doughnut: null }
      }
    },
    mounted () {
      this.fillData()
    },
    methods: {
      fillData () {
        this.datacollection.doughnut = {
          labels: [this.getRandomInt(), this.getRandomInt()],
          datasets: [
            {
              label: 'Data One',
              backgroundColor: ['#FFCEB3', '#849AB6', '#B5E29F', '#7FB6A7'],
              data: [this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt()]
            }
          ]
        }
        this.datacollection.line = {
          labels: [ 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May' ],
          datasets: [
            {
              label: 'Precipitation Levels 2017 (mm)',
              backgroundColor: '#086CA2',
              data: [ 26, 2, 5, 16, 111, 200, 254, 140, 75, 31, 20, 30 ]
            }
          ]
        }
      },
      getRandomInt () {
        return Math.floor(Math.random() * (50 - 5 + 1)) + 5
      }
    }
  }
</script>

<style>
  .small {
    max-width: 600px;
    /*margin:  150px auto;*/
  }
</style>
