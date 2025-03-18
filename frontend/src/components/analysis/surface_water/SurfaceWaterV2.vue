<template>
  <div id="surfaceWater">
    <v-row v-if="watershedLoading">
      <v-col>
        <div>Estimating catchment area...</div>
        <v-progress-linear indeterminate show></v-progress-linear>
      </v-col>
    </v-row>
    <v-row>
      <v-col class="pb-0">
        <v-alert type="info" dense class="my-1" outlined dismissible>
          This modelling output has not been peer reviewed and is still considered
          experimental. Use the values generated with your own discretion.
        </v-alert>
        <v-alert
          prominent
          type="error"
          outlined
          v-if="error.watershedList"
        >
          <v-row align="center">
            <v-col class="grow">
              Could not retrieve watershed data at this point.
              Note: this can sometimes occur if the point of interest is in a very large watershed.
              Please contact the Wally team for assistance.</v-col>
            <v-col class="shrink">
              <v-btn color="primary" @click="recalculateWatershed">Retry</v-btn>
            </v-col>
          </v-row>
        </v-alert>
      </v-col>
    </v-row>

    <v-card flat v-if="watersheds && watersheds.length" class="text-right">
      <SurfaceWaterHeaderButtons v-if="selectedWatershed" :layers="layers"/>
      <SavedAnalysesCreateModal :geometry="pointOfInterest.geometry" featureType="surface-water"/>
      <div class="watershedLabel"></div>
      <v-card flat >
        <v-card-title>
          {{watershedName}}
        </v-card-title>
        <v-card-text class="text-left">
          <v-row align="center">
            <v-col class="grow">
              {{watershedSource}}
            </v-col>
          </v-row>
          <v-row v-if="watershedWarnings.length">
            <v-col>
              <v-alert v-for="(w, i) in watershedWarnings" :key="`watershedWarning${i}`" type="info" dense outlined dismissible>
                {{w.message}}
              </v-alert>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-card>

    <template v-if="watersheds && watersheds.length">
      <div class="watershedInfo" v-if="selectedWatershed">
        <div v-if="watershedDetailsLoading">
          <div>Gathering data for selected catchment area...</div>
          <v-progress-linear indeterminate show></v-progress-linear>
        </div>
        <div v-else>
          <v-tabs
            vertical
            v-model="tab"
            dark
            show-arrows
          >
            <v-tab class="text-left">
              Watershed
            </v-tab>
            <v-tab class="text-left">
              Monthly Discharge
            </v-tab>
            <v-tab class="text-left" v-if="watershedDetails && watershedDetails.hydrometric_stations">
              Hydrometric Stations
            </v-tab>
            <v-tab class="text-left">
              Licenced Quantity
            </v-tab>
            <v-tab>
              Streamflow Report
            </v-tab>
            <v-tab>
              Runoff Models
            </v-tab>
            <v-tab class="text-left" v-if="showEfnAnalysisFlag">
              EFN
            </v-tab>
            <v-tab class="text-left">
              Fish Observations
            </v-tab>

            <!-- Watershed -->
            <v-tab-item>
              <WatershedDetails :modelOutputs="modelOutputs" :watershedName="watershedName" v-if="!error.watershedSummary"/>
              <v-card v-else flat>
                <v-card-text>
                  <v-alert
                    prominent
                    type="error"
                    outlined
                  >
                    <v-row align="center">
                      <v-col class="grow">
                        Could not calculate watershed summary data (area, precipitation, glacial coverage, estimated runoff) at this point.
                        Note: this can sometimes occur if the point of interest is in a very large watershed.
                        Please contact the Wally team for assistance.</v-col>
                      <v-col class="shrink">
                        <v-btn color="primary" @click="recalculateWatershed">Retry</v-btn>
                      </v-col>
                    </v-row>
                  </v-alert>
                </v-card-text>
              </v-card>
            </v-tab-item>
            <!-- Monthly Discharge -->
            <v-tab-item>
              <WatershedMonthlyDischarge
                :modelOutputs="modelOutputs"
                />
            </v-tab-item>

            <!-- Hydrometric Stations -->
            <v-tab-item eager>
              <HydrometricStationsContainer v-if="watershedDetails && watershedDetails.hydrometric_stations"
                                            :stations="watershedDetails.hydrometric_stations"
                                            :surface_water_design_v2="true"
              />
            </v-tab-item>

            <!-- Licenced Quantity -->
            <v-tab-item eager>
              <WatershedLicencedQty :modelOutputs="modelOutputs"
                                    :generatedWatershedID="generatedWatershedID"
                                    :watershedID="selectedWatershed"/>
            </v-tab-item>

            <!-- Streamflow Report -->
            <v-tab-item>
              <StreamflowInventory
                :coordinates="this.pointOfInterest.geometry.coordinates"
                :surface_water_design_v2="true"
              ></StreamflowInventory>
            </v-tab-item>

            <!-- Comparative Runoff Models -->
            <v-tab-item>
              <ComparativeRunoffModels :allWatersheds="watersheds"
                                       :record="selectedWatershedRecord"
                                       :surface_water_design_v2="true"/>
            </v-tab-item>

            <!-- EFN Analysis -->
            <v-tab-item v-if="showEfnAnalysisFlag">
              <EfnAnalysis />
            </v-tab-item>

            <!-- Known BC Fish Observations -->
            <v-tab-item>
              <FishObservations :watershedID="selectedWatershed"
                                :generatedWatershedID="generatedWatershedID"
                                :surface_water_design_v2="true"/>
            </v-tab-item>
          </v-tabs>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { mapGetters, mapMutations, mapActions } from 'vuex'
import ApiService from '../../../services/ApiService'
import qs from 'querystring'
import ComparativeRunoffModels from './ComparativeRunoffModels'
import HydrometricStationsContainer from './hydrometric_stations/HydrometricStationsContainer'
import FishObservations from './FishObservations'
import StreamflowInventory from './streamflow_inventory/StreamflowInventory'

import SurfaceWaterHeaderButtons from './SurfaceWaterHeaderButtons'
import WatershedDetails from './WatershedDetails'
import WatershedMonthlyDischarge from './WatershedMonthlyDischarge'
import WatershedLicencedQty from './watershed_demand/WatershedLicencedQty'

import EventBus from '../../../services/EventBus'

import { secondsInMonth } from '../../../constants/months'
import { findWallyLayer } from '../../../common/utils/mapUtils'
import { SOURCE_WATERSHEDS_AT_LOCATION } from '../../../common/mapbox/sourcesWally'
import SavedAnalysesCreateModal from '../../savedanalyses/SavedAnalysesCreateModal'
import EfnAnalysis from './efn_analysis/EfnAnalysis.vue'

export default {
  name: 'SurfaceWaterDetails',
  components: {
    HydrometricStationsContainer,
    ComparativeRunoffModels,
    FishObservations,
    StreamflowInventory,
    SurfaceWaterHeaderButtons,
    WatershedDetails,
    WatershedMonthlyDischarge,
    WatershedLicencedQty,
    SavedAnalysesCreateModal,
    EfnAnalysis
  },
  props: {
    upstreamMethod: {
      type: String,
      default: 'DEM+FWA'
    }
  },
  data: () => ({
    tab: null,
    infoTabs: null,
    watershedLoading: false,
    selectedWatershed: null,
    generatedWatershedID: null,
    assessmentWatershed: null,
    hydrometricWatershed: null,
    watersheds: [],
    watershedWarnings: [],
    geojsonLayersAdded: [],
    includePOIPolygon: false,
    watershedDetailsLoading: false,
    error: {
      watershedList: false,
      watershedSummary: false
    },
    spreadsheetLoading: false,
    shapefileLoading: false,
    modelOutputs: {
      mad: 0,
      mar: 0,
      low7q2: 0,
      dry7q10: 0,
      monthlyDischarges: [],
      monthlyDistributions: []
    },
    // These are the layers that are turned on by default for Surface Water Analysis
    layers: {
      hydrometric_stations: 'Hydrometric Stations',
      water_rights_licences: 'Water Rights Licences',
      water_approval_points: 'Water Approval Points',
      fish_observations: 'Known BC Fish Observations & Distributions',
      water_rights_applications: 'Water Rights Applications'
    }
  }),
  watch: {
    upstreamMethod: {
      deep: true,
      handler () {
        this.recalculateWatershed()
      }
    },
    selectedWatershed (v) {
      this.filterWatershed(v)
      this.fetchWatershedDetails()
    },
    includePOIPolygon () {
      this.recalculateWatershed()
    },
    watershedDetails: {
      immediate: true,
      handler (val, oldVal) {
        this.updateModelData(val)
      }
    }
  },
  computed: {
    watershedName () {
      if (!this.selectedWatershedRecord) {
        return ''
      }
      let name = ''
      const props = this.selectedWatershedRecord.properties
      name = props.GNIS_NAME_1
        ? props.GNIS_NAME_1
        : props.SOURCE_NAME
          ? props.SOURCE_NAME
          : props.name
            ? props.name
            : props.WATERSHED_FEATURE_ID
              ? props.WATERSHED_FEATURE_ID
              : props.OBJECTID ? props.OBJECTID : ''
      global.config.debug && console.log('[wally] name', name)
      return name.toString()
    },
    watershedSource () {
      if (!this.selectedWatershedRecord) {
        return ''
      }
      const id = this.selectedWatershedRecord.id
      if (id.includes('generated.')) {
        return 'Watershed estimated by combining Freshwater Atlas watershed polygons that are determined to be ' +
          'upstream of the point of interest based on their FWA_WATERSHED_CODE and LOCAL_WATERSHED_CODE properties.'
      }
      if (id.includes('WHSE_BASEMAPPING.FWA_ASSESSMENT_WATERSHEDS_POLY')) {
        return 'Watershed sourced from the "Freshwater Atlas Assessment Watersheds" layer in DataBC. ' +
          'https://catalogue.data.gov.bc.ca/dataset/freshwater-atlas-assessment-watersheds'
      }
      if (id.includes('WHSE_WATER_MANAGEMENT.HYDZ_HYD_WATERSHED_BND_POLY')) {
        return 'Watershed sourced from the "Hydrology: Hydrometric Watershed Boundaries" layer in DataBC. ' +
          'https://catalogue.data.gov.bc.ca/dataset/hydrology-hydrometric-watershed-boundaries'
      }
      return ''
    },
    selectedWatershedRecord () {
      if (!this.selectedWatershed || !this.watersheds) {
        return null
      }
      return this.watersheds.find((ws) => ws.id === this.selectedWatershed)
    },
    watershedOptions () {
      return this.watersheds.map((w, i) => ({
        label: (w.properties.GNIS_NAME_1 ||
          w.properties.SOURCE_NAME ||
          w.properties.name ||
          `Watershed ${i + 1}`).toLowerCase(),
        value: w.id
      }))
    },
    ...mapGetters('surfaceWater', ['watershedDetails', 'customModelInputsActive', 'scsb2016ModelInputs']),
    ...mapGetters(['pointOfInterest']),
    ...mapGetters('map', ['map']),
    ...mapGetters(['app']),
    showEfnAnalysisFlag () {
      return this.app && this.app.config && this.app.config.efn_analysis
    }
  },
  methods: {
    ...mapMutations('surfaceWater', ['setAvailabilityPlotData']),
    exportWatershedXLSX () {
      // Custom metrics - Track Excel downloads
      window._paq && window._paq.push([
        'trackLink',
        `${global.config.baseUrl}/api/v1/watersheds/${this.selectedWatershed}`,
        'download'])

      const params = {
        format: 'xlsx',
        generated_watershed_id: this.generatedWatershedID
      }

      this.spreadsheetLoading = true

      ApiService.query(`/api/v1/watersheds/${this.selectedWatershed}`,
        params, {
          responseType: 'arraybuffer'
        }).then((res) => {
        global.config.debug && console.log('[wally]', res)
        global.config.debug && console.log('[wally]', res.headers['content-disposition'])

        // default filename, and inspect response header Content-Disposition
        // for a more specific filename (if provided).
        let filename = 'SurfaceWater.xlsx'
        const filenameData = res.headers['content-disposition'] &&
          res.headers['content-disposition'].split('filename=')
        if (filenameData && filenameData.length === 2) {
          filename = filenameData[1]
        }

        const blob = new Blob([res.data], {
          type:
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })
        const link = document.createElement('a')
        link.href = window.URL.createObjectURL(blob)
        link.download = filename
        document.body.appendChild(link)
        link.click()
        setTimeout(() => {
          document.body.removeChild(link)
          window.URL.revokeObjectURL(link.href)
        }, 0)
        this.spreadsheetLoading = false
      }).catch((error) => {
        console.error(error)
        this.spreadsheetLoading = false
      })
    },
    exportWatershedShapefile () {
      // Custom metrics - Track Excel downloads
      window._paq && window._paq.push([
        'trackLink',
        `${global.config.baseUrl}/api/v1/watersheds/${this.selectedWatershed}`,
        'download'])

      const params = {
        format: 'shp',
        generated_watershed_id: this.generatedWatershedID
      }

      this.shapefileLoading = true

      ApiService.query(`/api/v1/watersheds/${this.selectedWatershed}`,
        params, {
          responseType: 'arraybuffer'
        }).then((res) => {
        global.config.debug && console.log('[wally]', res)
        global.config.debug && console.log('[wally]', res.headers['content-disposition'])

        // default filename, and inspect response header Content-Disposition
        // for a more specific filename (if provided).
        let filename = 'SurfaceWater.shp'
        const filenameData = res.headers['content-disposition'] &&
          res.headers['content-disposition'].split('filename=')
        if (filenameData && filenameData.length === 2) {
          filename = filenameData[1]
        }

        const blob = new Blob([res.data], {
          type:
            'application/zip'
        })
        const link = document.createElement('a')
        link.href = window.URL.createObjectURL(blob)
        link.download = filename
        document.body.appendChild(link)
        link.click()
        setTimeout(() => {
          document.body.removeChild(link)
          window.URL.revokeObjectURL(link.href)
        }, 0)
        this.shapefileLoading = false
      }).catch((error) => {
        console.error(error)
        this.shapefileLoading = false
      })
    },
    resetWatershed () {
      this.$store.dispatch('map/clearSelections')
      this.clearWatershedDetailsAndDefaults()

      // Clear URL params
      this.$router.push('surface-water')
    },
    filterWatershed (id) {
      this.geojsonLayersAdded.forEach((layerID) => {
        this.map.setLayoutProperty(
          layerID,
          'visibility',
          layerID.indexOf(`ws-${id}`) > -1 ? 'visible' : 'none'
        )
      })
    },
    addSingleWatershedLayer (data, id = 'watershedsAtLocation') {
      const layer = findWallyLayer(SOURCE_WATERSHEDS_AT_LOCATION)(id, data)
      this.map.addLayer(layer, 'water_rights_licences')
    },
    fetchWatersheds () {
      this.error.watershedList = false
      this.watershedLoading = true
      const params = {
        point: JSON.stringify(this.pointOfInterest.geometry.coordinates),
        include_self: this.includePOIPolygon,
        upstream_method: this.upstreamMethod
      }

      this.$router.push({
        query: { coordinates: this.pointOfInterest.geometry.coordinates }
      })

      ApiService.query(`/api/v1/watersheds/?${qs.stringify(params)}`)
        .then(r => {
          const data = r.data
          const ws = data.watershed
          this.generatedWatershedID = data.generated_watershed_id

          // an array of watersheds is used because there were previously
          // several different watershed options. Some components expect the array
          // plus the index of the selected watershed.
          // TODO: clean this up. We will probably only use one watershed from now on,
          // so an array is not necessary.
          this.watersheds = [ws]
          this.watershedWarnings = data.warnings || []

          this.selectedWatershed = ws.id
          this.addSingleWatershedLayer(ws, `ws-${ws.id}`)
          this.geojsonLayersAdded.push(`ws-${ws.id}`)

          this.watershedLoading = false
        })
        .catch(e => {
          this.error.watershedList = true
          this.watershedLoading = false
        })
    },
    fetchWatershedDetails () {
      this.error.watershedSummary = false
      this.watershedDetailsLoading = true
      const params = {
        generated_watershed_id: this.generatedWatershedID
      }
      ApiService.query(`/api/v1/watersheds/${this.selectedWatershed}?${qs.stringify(params)}`)
        .then(r => {
          this.watershedDetailsLoading = false
          if (!r.data) {
            return
          }
          // Set default watershed details/default model inputs
          this.initWatershedDetailsAndInputs(r.data)
        })
        .catch(e => {
          this.watershedDetailsLoading = false
          this.error.watershedSummary = true
        })
    },
    resetGeoJSONLayers () {
      this.watersheds.forEach((ws, i) => {
        this.map.removeLayer(`ws-${ws.id}`)
        this.map.removeSource(`ws-${ws.id}`)
      })
      this.watersheds = []
      this.geojsonLayersAdded = []
      this.selectedWatershed = null
      this.generatedWatershedID = null
      this.watershedWarnings = []
    },
    recalculateWatershed () {
      this.resetGeoJSONLayers()
      this.fetchWatersheds()
    },
    updateModelData (details) {
      // MAD Model Calculations
      if (!details) {
        return
      }

      if (details && details.scsb2016_model && !details.scsb2016_model.error) {
        const outputs = details.scsb2016_model
        const mar = outputs.find((x) => x.output_type === 'MAR')
        const mad = outputs.find((x) => x.output_type === 'MAD' && x.month === 0)
        const low7q2 = outputs.find((x) => x.output_type === '7Q2')
        const dry7q10 = outputs.find((x) => x.output_type === 'S-7Q10')
        const monthlyDistributions = outputs.filter((x) => x.output_type === 'MD')
        const monthlyDischarges = outputs.filter((x) => x.output_type === 'MAD' && x.month !== 0)
        this.modelOutputs = {
          sourceDescription: 'Model output based on South Coast Stewardship Baseline (Sentlinger, 2016).',
          mar: mar.model_result.toFixed(2),
          mad: mad.model_result.toFixed(2),
          low7q2: low7q2.model_result.toFixed(2),
          dry7q10: dry7q10.model_result.toFixed(2),
          monthlyDistributions,
          monthlyDischarges
        }
        const availability = monthlyDischarges.map((m) => { return m.model_result * secondsInMonth(m.month) })
        this.setAvailabilityPlotData(availability)
      } else {
        this.setAvailabilityPlotData(null)
      }
    },
    ...mapMutations('map', [
      'setMode'
    ]),
    ...mapMutations('surfaceWater', [
      'clearWatershedDetailsAndDefaults'
    ]),
    ...mapActions('surfaceWater', [
      'initWatershedDetailsAndInputs'
    ])
  },
  mounted () {
    this.setMode({ type: 'analyze', name: 'surface_water' })
    this.fetchWatersheds()
    EventBus.$on('watershed:reset', this.resetWatershed)
    EventBus.$on('watershed:export:pdf', this.downloadWatershedInfo)
    EventBus.$on('watershed:export:excel', this.exportWatershedXLSX)
    EventBus.$on('watershed:export:shp', this.exportWatershedShapefile)
  },
  beforeDestroy () {
    this.resetGeoJSONLayers()
    this.clearWatershedDetailsAndDefaults()
    this.setMode({ type: 'interactive', name: '' })
  }
}
</script>

<style>
#surfaceWater .info-blue .v-icon{
  color: teal;
}
#surfaceWater .info-blue {
  color: #085599;
}
#surfaceWater .v-card__title{
  font-size: 1rem
}
#surfaceWater .v-alert{
  font-size: .9rem
}
#surfaceWater .v-card__title.title{
  background-color: #085599;
  border-radius: 0;
  color: white;
}
#surfaceWater .v-tabs .v-item-group.v-tabs-bar {
  background-color: #085599;
}
</style>
