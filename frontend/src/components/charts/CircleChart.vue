<template>
  <div class="small">
        <doughnut-chart :chart-data="datacollection.doughnut"></doughnut-chart>
    <button @click="fillData()">Randomize</button>
  </div>
</template>

<script>
import DoughnutChart from './DoughnutChart.js'

export default {
  components: {
    DoughnutChart
  },
  data () {
    return {
      datacollection: { doughnut: null }
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
