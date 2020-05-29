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

    <!-- Licences -->
    <v-row>
      <v-col class="title">Water Rights Licences (Public) ({{licenceCount}})</v-col>
    </v-row>
    <v-row no-gutters >
      <v-col cols="12" md="4">
        <v-checkbox v-model="tableOptions.licences.subtypes.POD" class="mx-2" :label="`Point of diversion (POD) (${licenceSubtypeCounts.POD})`"></v-checkbox>
      </v-col>
      <v-col cols="12" md="4">
        <v-checkbox v-model="tableOptions.licences.subtypes.PWD" class="mx-2" :label="`Point of well diversion (PWD) (${licenceSubtypeCounts.PWD})`"></v-checkbox>
      </v-col>
      <v-col cols="12" md="4">
        <v-checkbox v-model="tableOptions.licences.subtypes.PG" class="mx-2" :label="`Point of groundwater diversion (PG) (${licenceSubtypeCounts.PG})`"></v-checkbox>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-data-table
          :loading="loading"
          :headers="licenceHeaders"
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
            <span v-if="item.QUANTITY" >{{item.QUANTITY }} {{item.QUANTITY_UNITS}}</span>
          </template>
        </v-data-table>
      </v-col>
    </v-row>

    <!-- Applications -->
    <div v-if="!loading">
      <v-row>
        <v-col class="title">Water Rights Applications (Public) ({{applicationCount}})</v-col>
      </v-row>
      <v-row no-gutters >
        <v-col cols="12" md="4">
          <v-checkbox v-model="tableOptions.applications.subtypes.POD" class="mx-2" :label="`Point of diversion (POD) (${applicationSubtypeCounts.POD})`"></v-checkbox>
        </v-col>
        <v-col cols="12" md="4">
          <v-checkbox v-model="tableOptions.applications.subtypes.PWD" class="mx-2" :label="`Point of well diversion (PWD) (${applicationSubtypeCounts.PWD})`"></v-checkbox>
        </v-col>
        <v-col cols="12" md="4">
          <v-checkbox v-model="tableOptions.applications.subtypes.PG" class="mx-2" :label="`Point of groundwater diversion (PG) (${applicationSubtypeCounts.PG})`"></v-checkbox>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-data-table
            :loading="loading"
            :headers="applicationHeaders"
            :items="filteredApplications"
          >
            <template v-slot:item.distance="{ item }">
              <span>{{item.distance.toFixed(1)}}</span>
            </template>
            <template v-slot:item.QUANTITY="{ item }">
              <span v-if="item.QUANTITY" >{{item.QUANTITY }} {{item.QUANTITY_UNITS}}</span>
            </template>
          </v-data-table>
        </v-col>
      </v-row>
    </div>

    <!-- Approvals -->
    <div v-if="!loading">
      <v-row>
        <v-col class="title">Water Approval Points ({{approvalCount}})</v-col>
      </v-row>
      <v-row no-gutters >
        <v-col cols="12" md="4">
          <v-checkbox v-model="tableOptions.approvals.current" class="mx-2" :label="`Current (${approvalStatusCounts.current})`"></v-checkbox>
        </v-col>
        <v-col cols="12" md="4">
          <v-checkbox v-model="tableOptions.approvals.expired" class="mx-2" :label="`Expired (${approvalStatusCounts.expired})`"></v-checkbox>
        </v-col>
        <v-col cols="12" md="4">
          <v-checkbox v-model="tableOptions.approvals.null" class="mx-2" :label="`Null or no status (${approvalStatusCounts.null})`"></v-checkbox>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-data-table
            :loading="loading"
            :headers="approvalHeaders"
            :items="filteredApprovals"
          >
            <template v-slot:item.distance="{ item }">
              <span>{{item.distance.toFixed(1)}}</span>
            </template>
            <template v-slot:item.QUANTITY="{ item }">
              <span v-if="item.QUANTITY" >{{item.QUANTITY}} {{item.QUANTITY_UNITS}}</span>
            </template>
          </v-data-table>
        </v-col>
      </v-row>
    </div>

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
              <p>Data on this page comes from <a href="https://catalogue.data.gov.bc.ca/dataset/water-rights-licences-public" target="_blank">Water Rights Licences (public)</a>,
              <a href="https://catalogue.data.gov.bc.ca/dataset/water-rights-applications-public" target="_blank">Water Rights Applications (public)</a>, and
              <a href="https://catalogue.data.gov.bc.ca/dataset/water-approval-points" target="_blank">Water Approval Points</a>.</p>
              <dl>
                <dt>Type</dt>
                <dd>Type indicates the data set that this record was found in; either Licence (Water Rights Licences), Application (Water Rights Applications), or an approval type such as CIAS, N-CIAS, or A-CIAS (Water Approval Points).</dd>
                <dt>Status</dt>
                <dd>Status comes from either LICENCE_STATUS (Water Rights Licences), APPLICATION_STATUS (Water Rights Applications), or APPROVAL_STATUS (Water Approval Points). See links to datasets on DataBC Catalogue above for more information.</dd>
                <dt>Licence number</dt>
                <dd>Licence number is the authorization number referenced in the water licence document, e.g., 121173.</dd>
                <dt>POD number</dt>
                <dd>POD number is the unique identifier for a Point of Diversion, e.g., PW189413. Each POD can have multiple licences associated with it.</dd>
                <dt>Usage type</dt>
                <dd>Usage type comes from either PURPOSE_USE (Water Rights Licences and Water Rights Applications), or WORKS_DESCRIPTION (Water Approval Points).</dd>
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
    licenceHeaders: [
      { text: 'Distance', value: 'distance' },
      { text: 'Type', value: 'type', filterable: true },
      { text: 'Licence number', value: 'LICENCE_NUMBER' },
      { text: 'Status', value: 'status', filterable: true },
      { text: 'POD number', value: 'POD_NUMBER' },
      { text: 'POD subtype', value: 'POD_SUBTYPE', filterable: true },
      { text: 'Usage type', value: 'usage', filterable: true },
      { text: 'Quantity', value: 'QUANTITY' }
    ],
    applicationHeaders: [
      { text: 'Distance', value: 'distance' },
      { text: 'Type', value: 'type', filterable: true },
      { text: 'Application number', value: 'APPLICATION_JOB_NUMBER' },
      { text: 'Status', value: 'status', filterable: true },
      { text: 'POD subtype', value: 'POD_SUBTYPE', filterable: true },
      { text: 'Usage type', value: 'usage', filterable: true },
      { text: 'Quantity', value: 'QUANTITY' }
    ],
    approvalHeaders: [
      { text: 'Distance', value: 'distance' },
      { text: 'Type', value: 'type', filterable: true },
      { text: 'Approval ID', value: 'WATER_APPROVAL_ID' },
      { text: 'File number', value: 'APPROVAL_FILE_NUMBER' },
      { text: 'Status', value: 'status', filterable: true },
      { text: 'Usage type', value: 'usage', filterable: true },
      { text: 'Quantity', value: 'QUANTITY' }
    ],
    tableOptions: {
      applications: {
        subtypes: {
          PWD: true,
          POD: true,
          PG: true
        }
      },
      approvals: {
        current: true,
        expired: true,
        null: true
      },
      licences: {
        subtypes: {
          PWD: true,
          POD: true,
          PG: true
        }
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
    filteredApprovals () {
      let approvals = this.results.filter(x => !!x.WATER_APPROVAL_ID)
      const opts = this.tableOptions.approvals

      const statusMap = {
        current: ['Current'],
        expired: ['Expired'],
        null: ['', null, '<Null>']
      }

      for (const key of Object.keys(opts)) {
        // check if this subtype key is disabled.
        if (!opts[key]) {
          approvals = approvals.filter(x => statusMap[key].indexOf(x.status) === -1)
        }
      }
      return approvals
    },
    filteredApplications () {
      let applications = this.results.filter(x => !!x.APPLICATION_JOB_NUMBER)
      const subtypes = this.tableOptions.applications.subtypes

      // loop through subtypes in tableOptions and if any subtype is disabled (false value),
      // filter it out of the licences array.
      for (const key of Object.keys(subtypes)) {
        // check if this subtype key is disabled.
        if (!subtypes[key]) {
          applications = applications.filter(x => x.POD_SUBTYPE !== key)
        }
      }

      return applications
    },
    filteredLicences () {
      let licences = this.results.filter(x => !!x.LICENCE_NUMBER)

      const subtypes = this.tableOptions.licences.subtypes

      // loop through subtypes in tableOptions and if any subtype is disabled (false value),
      // filter it out of the licences array.
      for (const key of Object.keys(subtypes)) {
        // check if this subtype key is disabled.
        if (!subtypes[key]) {
          licences = licences.filter(x => x.POD_SUBTYPE !== key)
        }
      }

      return licences
    },
    applicationCount () {
      return this.results.filter(x => !!x.APPLICATION_JOB_NUMBER).length
    },
    approvalCount () {
      return this.results.filter(x => !!x.WATER_APPROVAL_ID).length
    },
    licenceCount () {
      return this.results.filter(x => !!x.LICENCE_NUMBER).length
    },
    applicationSubtypeCounts () {
      const applications = this.results.filter(x => !!x.APPLICATION_JOB_NUMBER)
      const subtypes = this.tableOptions.applications.subtypes

      let counts = {}

      // loop through the subtypes, and count the number of each type.
      for (const key of Object.keys(subtypes)) {
        counts[key] = applications.filter(x => x.POD_SUBTYPE === key).length
      }
      return counts
    },
    approvalStatusCounts () {
      const approvals = this.results.filter(x => !!x.WATER_APPROVAL_ID)

      return {
        current: approvals.filter(x => x.status === 'Current').length,
        expired: approvals.filter(x => x.status === 'Expired').length,
        null: approvals.filter(x => x.status === '' || x.status === '<Null>' || !x.status).length
      }
    },
    licenceSubtypeCounts () {
      // counts each subtype in the results
      let licences = this.results.filter(x => !!x.LICENCE_NUMBER)
      const subtypes = this.tableOptions.licences.subtypes

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
      if (!this.radiusIsValid(this.radius)) {
        return
      }
      this.loading = true
      this.results = []

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
