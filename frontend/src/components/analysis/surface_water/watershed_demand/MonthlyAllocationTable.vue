<template>
  <v-dialog v-model="showEditDialog" persistent>
    <v-card>
      <v-card-title class="headline">
        Edit monthly allocation values
      </v-card-title>
      <v-card-text>Nam dictum fringilla velit et placerat. Aliquam ultricies massa gravida posuere ullamcorper. Duis fermentum purus felis. Duis fermentum lectus vel purus accumsan consectetur. Nunc suscipit mauris a eleifend consectetur. Vestibulum at odio lorem. Integer vel dignissim purus, nec pretium mi.</v-card-text>
      <v-simple-table>
        <template v-slot:default>
          <thead>
          <tr>
            <th width="300">Purpose Type</th>
            <th scope="col" class="text-left" v-for="month in months" :key="month">{{month}}</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(purposeType, i) in purposeTypes" :key="purposeType">
            <td>{{purposeType}}</td>
            <td v-for="(month, j) in months" :key="month">
              <v-text-field
                v-model="purposeTypeAllocationValues[i][j]"
              >
              </v-text-field>
            </td>
          </tr>
          </tbody>
        </template>
      </v-simple-table>
      <v-card-actions>
        <v-btn color="green darken-1" text @click="showEditDialog = false">Apply</v-btn>
        <v-btn color="green darken-1" text @click="exit">Cancel</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

</template>
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
    purposeTypeAllocationValues: []
  }),
  methods: {
    exit () {
      this.$emit('close', false)
    },
    populateTable () {
      this.purposeTypes = []
      this.purposeTypeQty = []
      console.log(this.qtyByPurpose)
      this.qtyByPurpose.forEach(item => {
        this.purposeTypes.push(item.purpose)
        this.purposeTypeQty.push(item.qty)
        let allocValues = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        this.purposeTypeAllocationValues.push(allocValues)
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
    }
  },
  mounted () {
    console.log('edit', this.edit)
    this.populateTable()
  }
}
</script>
