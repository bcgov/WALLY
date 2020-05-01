import moment from 'moment'
import { mapGetters, mapMutations, mapActions } from 'vuex'

export default {
  name: 'MonthlyAllocationTable',
  components: {
  },
  props: ['allocationItems', 'keyField'],
  data: () => ({
    months: moment.monthsShort(),
    allocItems: [],
    ...mapGetters('surfaceWater', ['allocationValues'])
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
          values: [...this.allocationValues()[allocItemKey] || defaultAllocValues]
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
        this.setAllocationValues({
          key: item.name,
          values: item.values })
      })

      // save to local storage
      this.$emit('close', false)
    },
    ...mapMutations('surfaceWater', [
      'setAllocationValues',
      'saveAllocationValues']),
    ...mapActions('surfaceWater', [
      'initAllocationItemIfNotExists',
      'computeQuantityForMonth'])
  },
  watch: {
    // edit (value) {
    //   this.showEditDialog = value
    // },
    allocationItems (value) {
      this.populateTable(value)
    },
    allocationValues (value) {
    }
  },
  mounted () {
    this.populateTable()
  }
}
