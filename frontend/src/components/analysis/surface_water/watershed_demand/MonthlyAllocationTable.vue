<template>
  <v-dialog v-model="showEditDialog" persistent>
    <v-card>
      <v-card-title class="headline">
        Edit monthly allocation values
        <v-spacer></v-spacer>
        <v-btn
          icon
          @click="exit"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text>Nam dictum fringilla velit et placerat. Aliquam ultricies massa gravida posuere ullamcorper. Duis fermentum purus felis. Duis fermentum lectus vel purus accumsan consectetur. Nunc suscipit mauris a eleifend consectetur. Vestibulum at odio lorem. Integer vel dignissim purus, nec pretium mi.</v-card-text>
      <v-simple-table>
        <template v-slot:default>
          <thead>
          <tr>
            <th scope="col" class="purpose-type">Purpose Type</th>
            <th scope="col" class="text-left alloc-value" v-for="month in months" :key="month">{{month}}</th>
            <th scope="col"></th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(purposeType, i) in purposeTypes" :key="purposeType">
            <td class="purpose-type">{{purposeType}}</td>
            <td v-for="(month, j) in months" :key="month">
              <v-text-field
                class="alloc-value"
                suffix="/12"
                dense
                filled
                v-model="purposeTypeAllocationValues[i][j]"
                hide-details="auto"
              >
              </v-text-field>
              <p class="font-weight-light caption text-right">
                {{purposeTypeAllocationValuesFraction[i][j].toFixed(2)}}
              </p>
<!--              <v-text-field-->
<!--                disabled-->
<!--                dense-->
<!--                v-model="purposeTypeAllocationValuesFraction[i][j]"-->
<!--              ></v-text-field>-->
            </td>
            <td>
              <v-chip>
                <v-avatar left
                >
                  <v-icon>mdi-check</v-icon>
                </v-avatar>
                {{purposeTypeAllocationValues[i].reduce((a, b) => (parseInt(a) || 0) + (parseInt(b) || 0), 0)}}
              </v-chip>
            </td>
          </tr>
          </tbody>
        </template>
      </v-simple-table>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary lighten-1" depressed @click="showEditDialog = false">Apply</v-btn>
        <v-btn color="grey" dark depressed @click="exit">Cancel</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

</template>
<style lang="scss">
  .purpose-type{
    width: 300px;
  }
  .alloc-value{
    width: 70px;
  }
  .v-text-field__suffix{
    font-size: smaller;
    opacity: 0.5;
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

    td.purpose-type {
      padding: 0 15px;
    }

    td:last-child{
      padding: 0 15px;
    }

  }
</style>
<script>
import moment from 'moment'

export default {
  name: 'MonthlyAllocationTable',
  components: {
  },
  props: ['edit', 'qtyByPurpose'],
  data: () => ({
    items: [],
    months: moment.monthsShort(),
    testRows: [1, 2, 3, 4, 5, 6, 7],
    showEditDialog: false,
    purposeTypes: [],
    purposeTypeQty: [],
    purposeTypeAllocationValues: [],
    purposeTypeAllocationValuesFraction: []
  }),
  methods: {
    exit () {
      this.$emit('close', false)
    },
    populateTable () {
      this.purposeTypes = []
      this.purposeTypeQty = []
      console.log(this.qtyByPurpose)
      let defaultFraction = 1 / 12
      this.qtyByPurpose.forEach(item => {
        this.purposeTypes.push(item.purpose)
        this.purposeTypeQty.push(item.qty)
        let allocValues = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        this.purposeTypeAllocationValues.push(allocValues)
        let allocValuesFraction = [defaultFraction, defaultFraction, defaultFraction, defaultFraction,
          defaultFraction, defaultFraction, defaultFraction, defaultFraction,
          defaultFraction, defaultFraction, defaultFraction, defaultFraction]
        this.purposeTypeAllocationValuesFraction.push(allocValuesFraction)
      })
      console.log(this.purposeTypes, this.purposeTypeQty, this.purposeTypeAllocationValues)
    }
  },
  watch: {
    edit (value) {
      this.showEditDialog = value
    },
    qtyByPurpose (value) {
      this.populateTable(value)
    },
    purposeTypeAllocationValues (value) {
      value.forEach((purposeType, i) => {
        purposeType.forEach((monthlyAllocationVal, j) => {
          this.purposeTypeAllocationValuesFraction[i][j] = this.purposeTypeAllocationValues[i][j] / 12
        })
      })
    },
    computeTotal (values) {
      return values.reduce((a, b) => (parseInt(a) || 0) + (parseInt(b) || 0), 0)
    }
  },
  mounted () {
    console.log('edit', this.edit)
    this.populateTable()
  }
}
</script>
