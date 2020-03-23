<template>
    <v-card id="editableModelCard">
      <v-card-title class="headline">
        Customize Model Inputs
        <v-spacer></v-spacer>
        <v-btn
          icon
          @click="exit"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text>
        <p>The watershed modeling inputs are pulled from various sources described by their info icons. The following inputs allow you to edit these values to allow for expert adjustment and discretion.</p>
      </v-card-text>
      <v-simple-table>
        <template v-slot:default>
          <thead>
          <tr>
            <th scope="col" class="text-left alloc-value" v-for="field in Object.keys(scsb2016ModelInputs)" :key="field">{{humanReadable(field)}}</th>
          </tr>
          </thead>
          <tbody>
            <tr>
              <td v-for="(item, i) in Object.keys(scsb2016ModelInputs)" :key="`${i}-${item}`">
                <v-text-field
                  dense
                  filled
                  hide-details="auto"
                  color="primary"
                  :rules="[inputRules.number, inputRules.required]"
                  v-model.number="scsb2016ModelInputs[item]"
                >
                </v-text-field>
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
import { mapGetters, mapMutations, mapActions } from 'vuex'
import qs from 'querystring'
import ApiService from '../../../services/ApiService'
import { humanReadable } from '../../../helpers'

export default {
  name: 'EditableModelInputs',
  components: {
  },
  props: [''],
  data: () => ({
    inputRules: {
      required: value => !!value || 'Required',
      number: value => !Number.isNaN(parseFloat(value)) || 'Invalid number'
    }
    // savingModelData: false
  }),
  methods: {
    exit () {
      this.$emit('close', false)
      // this.populateTable()
    },
    humanReadable: (val) => humanReadable(val),
    // populateTable () {
    //   this.allocItems = []
    //   this.modelInputs.forEach(item => {
    //     let itemKey = item[this.keyField].trim()
    //     let defaultAllocValues = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    //     this.allocItems.push({
    //       field: itemKey,
    //       values: [...this.allocationValues()[itemKey] || defaultAllocValues]
    //     })
    //   })
    // },
    saveValues () {
      // this.savingModelData = true
      ApiService.query(`/api/v1/scsb2016?${qs.stringify(this.scsb2016ModelInputs)}`)
        .then(r => {
          // this.savingModelData = false
          if (!r.data) {
            return
          }
          this.updateCustomScsb2016ModelData(r.data)
        })
        .catch(e => {
          // this.savingModelData = false
          console.error(e)
        })

      // save all allocation values to the store
      // this.allocItems.forEach(item => {
      //   this.setAllocationValues({
      //     key: item.name,
      //     values: item.values })
      // })

      this.$emit('close', false)
    },
    ...mapMutations('surfaceWater', [
      'setCustomModelInputs',
      'updateCustomScsb2016ModelData']),
    ...mapActions('surfaceWater', [
      'initAllocationItemIfNotExists']),
  },
  computed: {
    ...mapGetters('surfaceWater', ['scsb2016ModelInputs'])
  },
  watch: {
    // edit (value) {
    //   this.showEditDialog = value
    // },
    // modelInputs (value) {
    //   this.populateTable(value)
    // },
    // allocationValues (value) {
    // }
  },
  mounted () {
    // this.loadAllocationItemsFromStorage()
    // this.populateTable()
    // console.log("sASDFASDF!@#!#$@#$")
    // console.log(Object.keys(this.scsb2016ModelInputs))
    // console.log(Object.values(this.scsb2016ModelInputs))
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
