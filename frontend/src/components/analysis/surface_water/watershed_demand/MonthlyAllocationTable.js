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
    ...mapGetters('surfaceWater', ['allocationValues', 'test'])
  }),
  methods: {
    exit () {
      this.$emit('close', false)
    },
    populateTable () {
      this.allocationItems.forEach(item => {
        let allocItemKey = item[this.keyField].trim()
        let defaultAllocValues = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

        // Init allocation values if they don't exist
        this.initAllocationItemIfNotExists(allocItemKey)
        console.log('values would be', allocItemKey, this.test, this.allocationValues, this.allocationValues[allocItemKey])
        // TODO: Get values from store
        this.allocItems.push({
          name: allocItemKey,
          values: defaultAllocValues
        })
      })
      this.saveAllocationValues()
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
      this.saveAllocationValues()
      this.$emit('close', false)
    },
    ...mapMutations('surfaceWater', [
      'setAllocationValues',
      'saveAllocationValues']),
    ...mapActions('surfaceWater', [
      'initAllocationItemIfNotExists',
      'computeQuantityForMonth',
      'loadAllocationItemsFromStorage'])
  },
  watch: {
    // edit (value) {
    //   this.showEditDialog = value
    // },
    allocationItems (value) {
      this.populateTable(value)
    },
    allocationValues (value) {
      console.log('value', value)
    }
  },
  mounted () {
    this.loadAllocationItemsFromStorage()
    this.populateTable()
  }
}
