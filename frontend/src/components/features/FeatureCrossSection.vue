<template>
  <line-chart :chartData="featureData" :options="levelChartOptions"></line-chart>
</template>
<script>
export default {
  name: 'FeatureCrossSection',
  components: {
  },
  props: ['distance', 'elevations'],
  data: () => ({

  }),
  computed: {
    measurementData () {
      if (!this.distance || !this.elevations) {
        return { datasets: [] }
      }
      return {
        datasets: [
          {
            label: 'Measurement Analysis',
            lineTension: 0,
            fill: false,
            borderColor: '#1f548a',
            data: this.elevations
          }
        ]
      }
    }
  },
  measurementOptions (title, units, yValues) {
      return {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          yAxes: [{
            type: 'linear',
            ticks: {
              min: 0,
              max: Math.floor(Math.max.apply(Math, yValues) + 1),
              callback: function (value, index, values) {
                return `${value} ${units}`
              }
            }
          }],
          xAxes: [{
            type: 'linear',
            ticks: {
              min: 0,
              max: 12,
              callback: (value, index, values) => {
                return SHORT_MONTHS[value - 1]
              }
            }
          }]
        }
      }
    }
}
</script>

<style>

</style>