<template>
  <v-data-table
    :headers="headers"
    :items="months"
    :items-per-page="12"
    :item-class="risk"
    class="elevation-1"
  >
  </v-data-table>
</template>

<script>

export default {
  name: 'EfnAnalysisRiskTable',
  components: {
  },
  props: ['meanMonthlyDischarges', 'riskLevels'],
  data: () => ({
    headers: [
      {
        text: 'Month',
        align: 'start',
        sortable: false,
        value: 'month',
      },
      { text: 'MMD', value: 'mmd' },
      { text: 'Risk Level', value: 'risk' }
    ],
  }),
  computed: {
    months () {
      return this.meanMonthlyDischarges.map((mmd, idx) => {
        return {
          month: idx,
          mmd: mmd,
          risk: this.calculateRiskLevel(mmd)
        }
      })
      
    }
  },
  methods: {
    calculateRiskLevel (mmd) {
      return this.riskLevels.findIndex(riskLevel => mmd < riskLevel)
    }
  }
}
</script>

<style>
</style>
