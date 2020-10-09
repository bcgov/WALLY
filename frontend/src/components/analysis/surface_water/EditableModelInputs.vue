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
      <v-form
        ref="form"
        v-model="valid">
      <v-simple-table>

        <template v-slot:default>
          <thead>
          <tr>
            <th scope="col" class="">Model Input</th>
            <th scope="col" class="text-left input-value">Value</th>
            <th scope="col">Units</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(item, i) in Object.keys(scsb2016ModelInputValues)" :key="`${i}-${item}`">
            <th :id="`${item}`">
              {{humanReadable(item)}}
            </th>
            <td>
              <v-text-field
                dense
                filled
                hide-details="auto"
                color="primary"
                :rules="[inputRules.number]"
                v-model.number="scsb2016ModelInputValues[item]"
              >
              </v-text-field>
            </td>
            <td>
              {{inputUnits[item]}}
            </td>
          </tr>
          </tbody>
        </template>
      </v-simple-table>
      </v-form>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary lighten-1" depressed @click="saveValues">Apply</v-btn>
        <v-btn color="grey" dark depressed @click="reset">Reset</v-btn>
        <v-btn color="grey" dark depressed @click="exit">Cancel</v-btn>
      </v-card-actions>
    </v-card>
</template>

<script>
import { mapGetters, mapMutations, mapActions } from 'vuex'
import qs from 'querystring'
import ApiService from '../../../services/ApiService'
import { humanReadable } from '../../../common/helpers'

export default {
  name: 'EditableModelInputs',
  components: {
  },
  props: [''],
  data: () => ({
    valid: true,
    inputRules: {
      number: value => !Number.isNaN(parseFloat(value)) || 'Invalid number'
    },
    inputUnits: {
      hydrological_zone: '25, 26, 27',
      median_elevation: 'masl',
      glacial_coverage: '%',
      annual_precipitation: 'mm/yr',
      evapo_transpiration: 'mm/yr',
      drainage_area: 'km^2',
      solar_exposure: '%',
      average_slope: '%*100'
    },
    scsb2016ModelInputValues: {}
  }),
  methods: {
    exit () {
      this.$emit('close', false)
      this.populateForm()
    },
    inputsAreValid () {
      // const inputs = Object.values(this.scsb2016ModelInputValues)
      // const rules = Object.keys(this.inputRules)
      // for (let i = 0; i < inputs.length; i++) {
      //   for (let r = 0; r < rules.length; r++) {
      //     console.log(rules[r], inputs[i], this.inputRules[rules[r]](inputs[i]))
      //     if (this.inputRules[rules[r]](inputs[i]) !== true) {
      //       return false
      //     }
      //   }
      // }
      // return true
      // console.log(this.$refs.form.validate())
      return this.$refs.form.validate()
    },
    reset () {
      this.resetModelInputs()
      this.exit()
    },
    saveValues () {
      global.config.debug && console.log('[wally] Edit model inputs - Apply changes')
      if (!this.inputsAreValid()) {
        return
      }
      // TODO: save scsb2016ModelInputValues to scsb2016ModelInputs
      // Recalculate values from the API
      // Update Watershed Details
      this.setCustomModelInputs(this.scsb2016ModelInputValues)
      ApiService.query(`/api/v1/scsb2016/?${qs.stringify(this.scsb2016ModelInputs)}`)
        .then(r => {
          if (!r.data) {
            return
          }
          this.updateCustomScsb2016ModelData(r.data)
        })
        .catch(e => {
          console.error(e)
        })
      this.$emit('close', false)
    },
    populateForm () {
      this.scsb2016ModelInputValues = Object.assign({}, this.scsb2016ModelInputs)
    },
    ...mapMutations('surfaceWater', [
      'setCustomModelInputs',
      'updateCustomScsb2016ModelData']),
    ...mapActions('surfaceWater', ['resetModelInputs']),
    humanReadable: (val) => humanReadable(val)
  },
  computed: {
    ...mapGetters('surfaceWater', [
      'scsb2016ModelInputs'
    ])
  },
  mounted () {
    // console.log(Object.keys(this.scsb2016ModelInputs))
    // console.log(Object.values(this.scsb2016ModelInputs))
    this.populateForm()
  }
}
</script>

<style lang="scss">
  #editableModelCard {
    .input-value {
      width: 200px;
    }

    .v-text-field {
      input {
        text-align: right;
      }
    }

    .v-data-table {
      table {
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
      }

      td {
        padding: 0 2px;
      }

      td:first-child {
        padding-left: 20px;
      }
    }
  }
</style>
