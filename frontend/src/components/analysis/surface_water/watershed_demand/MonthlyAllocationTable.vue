<template>
  <v-dialog v-model="edit" persistent>
    <v-card>
      <v-card-title class="headline">
        Edit monthly allocation values
      </v-card-title>
      <v-card-text>Nam dictum fringilla velit et placerat. Aliquam ultricies massa gravida posuere ullamcorper. Duis fermentum purus felis. Duis fermentum lectus vel purus accumsan consectetur. Nunc suscipit mauris a eleifend consectetur. Vestibulum at odio lorem. Integer vel dignissim purus, nec pretium mi.</v-card-text>
      <v-simple-table>
        <template v-slot:default>
          <thead>
          <tr>
            <th scope="col" class="text-left" v-for="month in months" :key="month">{{month}}</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="row in [1,2,3,4,5]" :key="row">
            <td v-for="month in months" :key="month">
              <v-text-field
                v-model="testRows[row]"
              >
              </v-text-field>
            </td>
          </tr>
          </tbody>
        </template>
      </v-simple-table>
      <v-card-actions>
        <v-btn color="green darken-1" text @click="edit = false">Apply</v-btn>
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
  props: ['edit'],
  data: () => ({
    items: [],
    months: moment.months(),
    edit: this.props.edit,
    testRows: [1, 2, 3, 4, 5, 6, 7]
  }),
  methods: {
    exit () {
      this.edit = false
      this.$emit('close', false)
    }
  },
  mounted () {
  }
}
</script>
