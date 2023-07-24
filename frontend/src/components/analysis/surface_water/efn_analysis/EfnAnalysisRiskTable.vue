<template>
  <div>
    <v-data-table
      id="efn-risk-table"
      :headers="headers"
      hide-default-header
      disable-pagination
      :hide-default-footer="true"
      :items="months">
      <template v-slot:header="{ props: { headers } }">
        <thead>
          <tr>
            <th v-for="header in headers" v-bind:key="header.value" class="text-center">
              <v-tooltip top>
                <template v-slot:activator="{ on }">
                  <span v-on="on">{{header.text}}</span>
                </template>
                <span>{{header.tooltip}}</span>
              </v-tooltip>
            </th>
          </tr>
        </thead>
      </template>
      <template v-slot:item="{ item }">
        <tr>
          <td class="text-center v-data-table__divider pa-1" style="margin-left: auto; margin-right: auto;"><span>{{item.month}}</span></td>
          <td class="text-center v-data-table__divider pa-1"><span>{{item.mmd.toFixed(4)}}</span></td>
          <td class="text-center v-data-table__divider pa-1"><span>{{item.mmw.toFixed(4)}}</span></td>
          <td class="text-center v-data-table__divider pa-1"><span>{{(item.withdrawalPercent * 100).toFixed(2)}}%</span></td>
          <td class="text-center v-data-table__divider pa-1"><span>{{item.sensitivity}}</span></td>
          <td :style="{backgroundColor: riskSchema[item.risk].color, color: 'white'}" class="text-center v-data-table__divider pa-2"><span>{{riskSchema[item.risk].name}}</span></td>
        </tr>
      </template>
    </v-data-table>
    <EfnAnalysisMonthlyQty
      :mmd="waterFlowData.mmd"
      :mad="waterFlowData.mad"
      :licenceData="licenceWithdrawalData"
      :riskLevels="monthRiskThresholds"
    />
  </div>
</template>

<script>
import EfnAnalysisMonthlyQty from './EfnAnalysisMonthlyQty'

export default {
  name: 'EfnAnalysisRiskTable',
  components: {
    EfnAnalysisMonthlyQty
  },
  props: ['waterFlowData', 'licenceWithdrawalData', 'fishBearing'],
  data: () => ({
    headers: [
      {
        text: 'Month',
        align: 'start',
        sortable: false,
        value: 'month',
        tooltip: 'Month of the year'
      },
      {
        text: 'MMD m3/s',
        value: 'mmd',
        tooltip: 'Mean Monthly Drainage'
      },
      {
        text: 'MMW m3/s',
        value: 'mmw',
        tooltip: 'Mean Monthly Withdrawal'
      },
      {
        text: 'Withdrawal %',
        value: 'withdrawalPercent',
        tooltip: 'Allocated licence withdrawal amount for this month'
      },
      {
        text: 'Flow Sensitivity',
        value: 'sensitivity',
        tooltip: 'Sensitivity is based on mean monthly flow over MAD'
      },
      {
        text: 'Risk Level',
        value: 'risk',
        tooltip: 'EFN risk level associated with withdrawals'
      }
    ],
    riskCategories: {
      lowSensitivity: {
        sensitivity: 'Low',
        thresholds: [0.15, 0.20, 1.0]
      },
      moderateSensitivitySmallStream: {
        sensitivity: 'Moderate',
        thresholds: [0, 0.1, 1.0]
      },
      moderateSensitivityMediumLargeStream: {
        sensitivity: 'Moderate',
        thresholds: [0.1, 0.15, 1.0]
      },
      highSensitivitySmallStream: {
        sensitivity: 'High',
        thresholds: [0, 0.05, 1.0]
      },
      highSensitivityMediumLargeStream: {
        sensitivity: 'High',
        thresholds: [0.05, 0.1, 1.0]
      }
    },
    monthHeaders: [
      { text: 'Jan', value: 'm1' },
      { text: 'Feb', value: 'm2' },
      { text: 'Mar', value: 'm3' },
      { text: 'Apr', value: 'm4' },
      { text: 'May', value: 'm5' },
      { text: 'Jun', value: 'm6' },
      { text: 'Jul', value: 'm7' },
      { text: 'Aug', value: 'm8' },
      { text: 'Sep', value: 'm9' },
      { text: 'Oct', value: 'm10' },
      { text: 'Nov', value: 'm11' },
      { text: 'Dec', value: 'm12' }
    ],
    riskSchema: [
      {
        name: 'Low',
        color: '#62C370'
      },
      {
        name: 'Medium',
        color: '#EFA00B'
      },
      {
        name: 'High',
        color: '#EF2917'
      }
    ],
    monthRiskThresholds: []
  }),
  computed: {
    months () {
      this.resetMonthRiskThresholds()
      return this.waterFlowData.mmd.map((mmd, idx) => {
        const { riskCategory, thresholdIndex } = this.calculateRiskLevel(mmd, idx)
        this.updateMonthRiskThresholds(riskCategory.thresholds)
        return {
          month: this.monthHeaders[idx].text,
          mmd: mmd,
          mmw: this.meanMonthlyWithdrawal(idx),
          withdrawalPercent: this.monthlyWithdrawalPercent(mmd, idx),
          sensitivity: riskCategory.sensitivity,
          risk: thresholdIndex
        }
      })
    }
  },
  methods: {
    resetMonthRiskThresholds () {
      this.monthRiskThresholds = []
    },
    updateMonthRiskThresholds (thresholds) {
      this.monthRiskThresholds.push(thresholds)
    },
    meanMonthlyWithdrawal (month) {
      // Mean withdrawl amount for this month
      return this.licenceWithdrawalData.longTerm[month] + this.licenceWithdrawalData.shortTerm[month]
    },
    monthlyWithdrawalPercent (mmd, month) {
      const mmw = this.meanMonthlyWithdrawal(month)

      // Correct negative values to zero.
      // Depending on the inputs and the model, the monthly discharge may be slightly negative.
      // If this is an error or a bug to be reported, it will still be visible to the user in other columns.
      mmd = Math.max(mmd, 0)

      // if no withdrawal, set monthly withdrawal % to zero regardless of what monthly flow is.
      if (mmw === 0) {
        return 0
      }

      // if no discharge and non-zero withdrawal, call withdrawal percent infinity.
      if (mmd === 0) {
        return Infinity
      }

      const withdrawalPercent = mmw / mmd
      return withdrawalPercent
    },
    calculateRiskLevel (mmd, month) {
      const mad = this.waterFlowData.mad
      const isSmallStream = mad < 10

      // Relative monthly flow is the ratio between the mean monthly flow and MAD
      const relativeMonthlyFlow = mmd / mad

      // Find the risk category for this month
      let riskCategory = this.riskCategories.lowSensitivity
      if (this.fishBearing) {
        if (relativeMonthlyFlow >= 0.2) { // Low sensitivity
          riskCategory = this.riskCategories.lowSensitivity
        } else if (relativeMonthlyFlow >= 0.1 && relativeMonthlyFlow < 0.2) { // Moderate sensitivity
          if (isSmallStream) {
            riskCategory = this.riskCategories.moderateSensitivitySmallStream
          } else {
            riskCategory = this.riskCategories.moderateSensitivityMediumLargeStream
          }
        } else if (relativeMonthlyFlow < 0.1) { // High sensitivity
          if (isSmallStream) {
            riskCategory = this.riskCategories.highSensitivitySmallStream
          } else {
            riskCategory = this.riskCategories.highSensitivityMediumLargeStream
          }
        }
      }
      // Get risk level for this month
      let thresholdIndex = riskCategory.thresholds.findIndex(riskThreshold =>
        this.monthlyWithdrawalPercent(mmd, month) < riskThreshold)
      if (thresholdIndex === -1) { thresholdIndex = 2 }

      return { riskCategory, thresholdIndex }
    },
    riskStyle (risk) {
      return this.riskColors[risk]
    }
  }
}
</script>

<style>
</style>
