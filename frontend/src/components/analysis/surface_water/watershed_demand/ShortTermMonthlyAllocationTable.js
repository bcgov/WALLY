import moment from 'moment'
import { mapGetters, mapMutations, mapActions } from 'vuex'

export default {
  name: 'ShortTermMonthlyAllocationTable',
  components: {
  },
  props: ['allocationItems', 'keyField'],
  data: () => ({
    months: moment.monthsShort(),
    allocItems: [],
    ...mapGetters('surfaceWater', ['shortTermAllocationValues'])
  }),
  methods: {
    exit () {
      this.$emit('close', false)
      this.populateTable()
    },
    populateTable () {
      this.allocItems = []
      this.allocationItems.forEach(item => {
        let allocItemKey = item[this.keyField].trim()
        let defaultAllocValues = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

        this.allocItems.push({
          name: allocItemKey,
          values: [...this.shortTermAllocationValues()[allocItemKey] || defaultAllocValues]
        })
      })
    },
    computeRowTotal (values) {
      return values.reduce((a, b) => (parseInt(a) || 0) + (parseInt(b) || 0), 0)
    },
    computeDecimal (value) {
      return !isNaN(value) && value / 12
    },
    saveValues () {
      // save all allocation values to the store
      this.allocItems.forEach(item => {
        this.setShortTermAllocationValues({
          key: item.name,
          values: item.values })
      })

      // save to local storage
      this.$emit('close', false)
    },
    ...mapMutations('surfaceWater', [
      'setShortTermAllocationValues',
      'saveShortTermAllocationValues']),
    ...mapActions('surfaceWater', [
      'initShortTermAllocationItemIfNotExists',
      'computeQuantityForMonth'])
  },
  watch: {
    allocationItems (value) {
      this.populateTable(value)
    },
    shortTermAllocationValues (value) {
    }
  },
  mounted () {
    this.populateTable()
  }
}
