export default {
  methods: {
    computeMonthlyQuantities (qtyPerYear, allocationValues) {
      let monthlyQty
      let allQty = []
      for (let i = 0; i < 12; i++) {
        monthlyQty = this.computeQuantityForMonth(qtyPerYear, allocationValues, i + 1)
        allQty.push(monthlyQty)
      }
      return allQty
    },
    computeQuantityForMonth (qtyPerYear, allocationValues, month) {
      let allocFraction = Number(allocationValues[month - 1])
      return qtyPerYear * (allocFraction / 12)
    }
  }
}
