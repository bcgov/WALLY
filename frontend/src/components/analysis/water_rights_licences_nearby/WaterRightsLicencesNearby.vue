<template>
  <v-container>
    <v-row no-gutters>
      <v-col cols="12" md="4" align-self="center">
        <v-text-field
          label="Search radius (m)"
          placeholder="1000"
          :rules="[inputRules.number, inputRules.max, inputRules.required]"
          v-model="radius"
        ></v-text-field>
      </v-col>
      <v-col class="text-right">
          <v-btn
            v-if="filteredLicences.length"
            outlined
            :disabled="loading"
            @click="exportLicencesAsSpreadsheet"
            color="primary"
          >
            Excel
            <v-icon class="ml-1" v-if="!spreadsheetLoading">cloud_download</v-icon>
            <v-progress-circular
              v-if="spreadsheetLoading"
              indeterminate
              size=24
              class="ml-1"
              color="primary"
            ></v-progress-circular>
          </v-btn>
      </v-col>
    </v-row>
    <v-row no-gutters >
      <v-col cols="12" md="4">
        <v-checkbox v-model="tableOptions.subtypes.POD" class="mx-2" :label="`Point of diversion (POD) (${subtypeCounts.POD})`"></v-checkbox>
      </v-col>
      <v-col cols="12" md="4">
        <v-checkbox v-model="tableOptions.subtypes.PWD" class="mx-2" :label="`Point of well diversion (PWD) (${subtypeCounts.PWD})`"></v-checkbox>
      </v-col>
      <v-col cols="12" md="4">
        <v-checkbox v-model="tableOptions.subtypes.PG" class="mx-2" :label="`Point of groundwater diversion (PG) (${subtypeCounts.PG})`"></v-checkbox>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col cols="12" md="4">
        <v-checkbox v-model="tableOptions.applications" class="mx-2" :label="`Water Rights Applications (${applicationCount})`"></v-checkbox>
      </v-col>
      <v-col cols="12" md="4">
        <v-checkbox v-model="tableOptions.approvals" class="mx-2" :label="`Water Approval Points (${approvalCount})`"></v-checkbox>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-data-table
          :loading="loading"
          :headers="headers"
          :items="filteredLicences"
        >
          <template v-slot:item.LICENCE_NUMBER="{ item }">
            <span v-if="item.LICENCE_NUMBER">
              <a :href="`https://j200.gov.bc.ca/pub/ams/Default.aspx?PossePresentation=AMSPublic&amp;PosseObjectDef=o_ATIS_DocumentSearch&amp;PosseMenuName=WS_Main&Criteria_LicenceNumber=${item.LICENCE_NUMBER}`" target="_blank">
                {{item.LICENCE_NUMBER}}
              </a>
            </span>
          </template>
          <template v-slot:item.distance="{ item }">
            <span>{{item.distance.toFixed(1)}}</span>
          </template>
          <template v-slot:item.QUANTITY="{ item }">
            <span v-if="item.QUANTITY" >{{item.QUANTITY.toFixed(3)}} {{item.QUANTITY_UNITS}}</span>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-expansion-panels class="mt-5 elevation-0" multiple>
          <v-expansion-panel class="elevation-0">
            <v-expansion-panel-header disable-icon-rotate class="grey--text text--darken-4 subtitle-1">
              Where does this information come from?
              <template v-slot:actions>
                <v-icon color="primary">mdi-help-circle-outline</v-icon>
              </template>

            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <p>Data on this page comes from <a href="https://catalogue.data.gov.bc.ca/dataset/water-rights-licences-public" target="_blank">Water Rights Licences (public)</a>.</p>
              <dl>
                <dt>Licence number</dt>
                <dd>Licence number is the authorization number referenced in the water licence document, e.g., 121173.</dd>
                <dt>POD number</dt>
                <dd>POD number is the unique identifier for a Point of Diversion, e.g., PW189413. Each POD can have multiple licences associated with it.</dd>
                <dt>Purpose use</dt>
                <dd>Purpose use is the use of water authorized by the licence, e.g. Industrial.</dd>
                <dt>Quantity</dt>
                <dd>Quantity is the maximum quantity of water that is authorized to be diverted for the purpose use, e.g., 500 m3/day.</dd>
                <dt>POD subtype</dt>
                <dd>
                  POD subtype distinguishes the different POD types, i.e., POD (a surface water point of diversion), PWD (a point of well diversion that diverts groundwater),
                  or PG (a point of groundwater diversion that diverts groundwater such as a dugout, ditch or quarry).
                </dd>
              </dl>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import qs from 'querystring'
import ApiService from '../../../services/ApiService'
import debounce from 'lodash.debounce'
import circle from '@turf/circle'

export default {
  name: 'WaterRightsLicencesNearby',
  props: ['record'],
  data: () => ({
    inputRules: {
      required: value => !!value || 'Required',
      number: value => !Number.isNaN(parseFloat(value)) || 'Invalid number',
      max: value => value <= 10000 || 'Radius must be between 0 and 10000 m'
    },
    radius: 1000,
    results: [],
    loading: false,
    spreadsheetLoading: false,
    licencesLayerAutomaticallyEnabled: false,
    applicationsLayerAutomaticallyEnabled: false,
    approvalsLayerAutomaticallyEnabled: false,
    headers: [
      { text: 'Distance', value: 'distance' },
      { text: 'Type', value: 'type' },
      { text: 'Application number', value: 'APPLICATION_JOB_NUMBER' },
      { text: 'Status', value: 'status' },
      { text: 'Licence number', value: 'LICENCE_NUMBER' },
      { text: 'POD number', value: 'POD_NUMBER' },
      { text: 'POD subtype', value: 'POD_SUBTYPE', filterable: true },
      { text: 'Purpose use', value: 'PURPOSE_USE' },
      { text: 'Quantity', value: 'QUANTITY' }
    ],
    tableOptions: {
      applications: true,
      approvals: true,
      subtypes: {
        PWD: true,
        POD: true,
        PG: true
      }

    }
  }),
  computed: {
    isLicencesLayerEnabled () {
      return this.isMapLayerActive('water_rights_licences')
    },
    isApplicationsLayerEnabled () {
      return this.isMapLayerActive('water_rights_applications')
    },
    isApprovalsLayerEnabled () {
      return this.isMapLayerActive('water_approval_points')
    },
    coordinates () {
      return this.record && this.record.geometry && this.record.geometry.coordinates
    },
    filteredLicences () {
      let licences = this.results

      const subtypes = this.tableOptions.subtypes

      // loop through subtypes in tableOptions and if any subtype is disabled (false value),
      // filter it out of the licences array.
      for (const key of Object.keys(subtypes)) {
        // check if this subtype key is disabled.
        if (!subtypes[key]) {
          licences = licences.filter(x => x.POD_SUBTYPE !== key)
        }
      }

      // use the property APPLICATION_JOB_NUMBER to determine if this point is an application.
      // see https://catalogue.data.gov.bc.ca/dataset/water-rights-applications-public
      if (!this.tableOptions.applications) {
        licences = licences.filter(x => !x.APPLICATION_JOB_NUMBER)
      }

      // use the property WATER_APPROVAL_ID to determin if this point is a water approval (section 10
      // or section 11 approvals).
      // https://catalogue.data.gov.bc.ca/dataset/water-approval-points
      if (!this.tableOptions.approvals) {
        licences = licences.filter(x => !x.WATER_APPROVAL_ID)
      }

      return licences
    },
    applicationCount () {
      return this.results.filter(x => !!x.APPLICATION_JOB_NUMBER).length
    },
    approvalCount () {
      return this.results.filter(x => !!x.WATER_APPROVAL_ID).length
    },
    subtypeCounts () {
      // counts each subtype in the results
      let licences = this.results
      const subtypes = this.tableOptions.subtypes

      let counts = {}

      // loop through the subtypes, and count the number of each type.
      for (const key of Object.keys(subtypes)) {
        counts[key] = licences.filter(x => x.POD_SUBTYPE === key).length
      }
      return counts
    },
    ...mapGetters('map', ['isMapLayerActive'])
  },
  methods: {
    addMissingMapLayers () {
      if (!this.isLicencesLayerEnabled) {
        this.$store.dispatch('map/addMapLayer', 'water_rights_licences')
        this.licencesLayerAutomaticallyEnabled = true
      }
      if (!this.isApplicationsLayerEnabled) {
        this.$store.dispatch('map/addMapLayer', 'water_rights_applications')
        this.applicationsLayerAutomaticallyEnabled = true
      }
      if (!this.isApprovalsLayerEnabled) {
        this.$store.dispatch('map/addMapLayer', 'water_approval_points')
        this.approvalsLayerAutomaticallyEnabled = true
      }
    },
    removeAutomaticallyAddedLayers () {
      if (this.licencesLayerAutomaticallyEnabled) {
        this.$store.dispatch('map/removeMapLayer', 'water_rights_licences')
      }
      if (this.applicationsLayerAutomaticallyEnabled) {
        this.$store.dispatch('map/removeMapLayer', 'water_rights_applications')
      }
      if (this.approvalsLayerAutomaticallyEnabled) {
        this.$store.dispatch('map/removeMapLayer', 'water_rights_approvals')
      }
    },
    fetchLicences: debounce(function () {
      this.showCircle()
      this.loading = true
      if (!this.radiusIsValid(this.radius)) {
        return
      }

      // turn on licences, applications and approvals map layer
      this.addMissingMapLayers()

      const params = {
        radius: parseFloat(this.radius),
        point: JSON.stringify(this.coordinates)
      }
      ApiService.query(`/api/v1/licences/nearby?${qs.stringify(params)}`).then((r) => {
        this.results = r.data
      }).catch((e) => {
        console.error(e)
      }).finally(() => {
        this.loading = false
      })
    }, 500),
    radiusIsValid (val) {
      let invalid = Object.keys(this.inputRules).some((k) => {
        return this.inputRules[k](val) !== true
      })
      return !invalid
    },
    exportLicencesAsSpreadsheet () {
      this.spreadsheetLoading = true
      const params = {
        radius: parseFloat(this.radius),
        point: JSON.stringify(this.coordinates),
        format: 'xlsx'
      }
      if (!this.radiusIsValid(this.radius)) {
        return
      }
      ApiService.query(`/api/v1/licences/nearby`, params, { responseType: 'arraybuffer' }).then((r) => {
        // default filename, and inspect response header Content-Disposition
        // for a more specific filename (if provided).
        let filename = 'WaterLicences.xlsx'
        const filenameData = r.headers['content-disposition'] && r.headers['content-disposition'].split('filename=')
        if (filenameData && filenameData.length === 2) {
          filename = filenameData[1]
        }

        let blob = new Blob([r.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
        let link = document.createElement('a')
        link.href = window.URL.createObjectURL(blob)
        link.download = filename
        document.body.appendChild(link)
        link.click()
        setTimeout(() => {
          document.body.removeChild(link)
          window.URL.revokeObjectURL(link.href)
        }, 0)
      }).catch((e) => {
        console.error(e)
      }).finally(() => {
        this.spreadsheetLoading = false
      })
    },
    showCircle () {
      const options = { steps: 32, units: 'kilometers', properties: { display_data_name: 'user_search_radius' } }
      const radius = this.radius / 1000
      const shape = circle(this.coordinates, radius, options)
      shape.id = 'user_search_radius'

      // remove old shapes
      this.$store.commit('map/removeShapes')

      // add the new one
      this.$store.commit('map/addShape', shape)
    }
  },
  watch: {
    record: {
      handler () {
        this.fetchLicences()
      },
      deep: true
    },
    coordinates () {
      this.fetchLicences()
    },
    radius (value) {
      this.fetchLicences()
    }
  },
  mounted () {
    this.fetchLicences()
  },
  beforeDestroy () {
    this.removeAutomaticallyAddedLayers()
    this.$store.commit('map/removeShapes')
    this.$store.dispatch('map/clearSelections')
  }
}
</script>

<style>
label.theme--light.v-label {
  color: rgba(0,0,0,.87)
}
</style>
