<template>
    <v-card id="allocationTable">
      <v-card-title class="headline">
        Configure short term monthly allocation values
        <v-spacer></v-spacer>
        <v-btn
          icon
          @click="exit"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text>
        <p>The short term allocation volume can be distributed differently over 12 months of a year. To reflect variations in the monthly demand, a coefficient can be applied based on the proportion of distribution over the year. For example, a short term approval may only be valid for between April 1 and September 30. Therefore, it could be assigned a value of 2/12 between April and September, and 0/12 between October and March.</p>
        <!-- <p>Edit the short monthly allocation coefficient values by re-distributing the expected annual proportion of approved water quantity in the table below. Values allocated monthly should total 12 to indicate an annual allocation distribution.</p> -->
      </v-card-text>
      <v-simple-table>
        <template v-slot:default>
          <thead>
          <tr>
            <th scope="col" class="alloc-item">Approval Number</th>
            <th scope="col" class="text-left alloc-value" v-for="month in months" :key="month">{{month}}</th>
            <th scope="col"></th>
          </tr>
          </thead>
          <tbody>
            <tr v-for="(item, i) in allocItems" :key="`${i}-${item.name}`">
              <td>{{item.name}}</td>
              <td v-for="(month, j) in months" :key="`${j}-${month}`">
                <v-text-field
                  class="alloc-value"
                  suffix="/12"
                  dense
                  filled
                  v-model="item.values[j]"
                  hide-details="auto"
                  color="primary"
                >
                </v-text-field>
              <p class="font-weight-light caption text-right">
                {{computeDecimal(item.values[j]) | formatNumber}}
              </p>
              </td>
            <td>
              <v-chip small :color="(computeRowTotal(item.values) === 12)?'green lighten-3': 'red lighten-3'">
                <v-avatar left
                >
                  <v-icon small v-if="computeRowTotal(item.values) === 12">mdi-check</v-icon>
                  <v-icon small v-else>mdi-close</v-icon>
                </v-avatar>
                {{computeRowTotal(item.values)}}
              </v-chip>
            </td>
          </tr>
          </tbody>
        </template>
      </v-simple-table>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary lighten-1" depressed @click="saveValues">Apply</v-btn>
        <v-btn color="grey" dark depressed @click="exit">Cancel</v-btn>
      </v-card-actions>
    </v-card>
</template>

<script>
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
      // for (let [allocItemKey, allocValues] of Object.entries(this.allocationItems)) {
      this.allocationItems.forEach(item => {
        let allocItemKey = item[this.keyField].trim()
        let defaultAllocValues = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        this.allocItems.push({
          name: allocItemKey,
          values: this.shortTermAllocationValues[allocItemKey] || defaultAllocValues
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
      'setShortTermAllocationValues']),
    ...mapActions('surfaceWater', [
      'initShortTermAllocationItemIfNotExists',
      'computeQuantityForMonth'])
  },
  watch: {
    // shortTermAllocationItems (value) {
    //   this.populateTable(value)
    // }
  },
  mounted () {
    this.populateTable()
  }
}
</script>

<style lang="scss">
  .alloc-item{
    width: 300px;
  }
  .alloc-value{
    width: 70px;
  }
  .v-text-field__suffix{
    font-size: smaller;
    opacity: 0.2;
  }
  .v-text-field{
    input {
      text-align: right;
    }
  }
  .v-data-table {
    td {
      padding: 0 2px;
    }

    td:first-child{
      padding-left: 20px;
    }

    td.purpose-type {
      padding: 0 15px;
    }

    td:last-child{
      padding: 10px 15px;
      vertical-align: top;
    }

  }
</style>
