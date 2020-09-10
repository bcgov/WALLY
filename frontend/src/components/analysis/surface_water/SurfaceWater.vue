<template>
  <div>
    <v-row>
      <v-col class="pb-0">
        <v-alert type="info" dense class="mb-0" outlined dismissible>
          This modelling output has not been peer reviewed and is still considered
          experimental. Use the values generated with your own discretion.
        </v-alert>
      </v-col>
    </v-row>

    <v-card flat v-if="watersheds && watersheds.length">

      <SurfaceWaterHeaderButtons v-on:reset-watershed="resetWatershed"/>
      <v-select
        v-model="selectedWatershed"
        :items="watershedOptions"
        :menu-props="{ maxHeight: '400' }"
        label="Watershed"
        item-text="label"
        item-value="value"
        hint="Select from available watersheds at this location"
      ></v-select>
    </v-card>

    <template v-if="watersheds && watersheds.length">
      <div v-if="selectedWatershed">
        <div v-if="watershedDetailsLoading">
          <v-progress-linear indeterminate show></v-progress-linear>
        </div>
        <div v-else>
          <v-tabs
            vertical
            v-model="tab"
            background-color="blue darken-4"
            dark
            show-arrows
          >
            <v-tab class="text-left">
              Watershed
            </v-tab>
            <v-tab class="text-left">
              Monthly Discharge
            </v-tab>
            <v-tab class="text-left">
              Licenced Quantity
            </v-tab>
            <v-tab class="text-left" v-if="watershedDetails && watershedDetails.hydrometric_stations">
              Hydrometric Stations
            </v-tab>
            <v-tab>
              Streamflow Report
            </v-tab>
            <v-tab class="text-left">
              Fish Observations
            </v-tab>
            <v-tab class="text-left">
              FIDQ
            </v-tab>
            <v-tab>
              Runoff Models
            </v-tab>

            <!-- Watershed -->
            <v-tab-item>
              <WatershedDetails :modelOutputs="modelOutputs"/>
            </v-tab-item>
            <!-- Monthly Discharge -->
            <v-tab-item>
              <WatershedMonthlyDischarge :modelOutputs="modelOutputs"/>
            </v-tab-item>

            <!-- Licenced Quantity -->
            <v-tab-item>
              <WatershedLicencedQty :modelOutputs="modelOutputs"
                                    :watershedID="selectedWatershed"/>
            </v-tab-item>

            <!-- Hydrometric Stations -->
            <v-tab-item>
              <HydrometricStationsContainer v-if="watershedDetails && watershedDetails.hydrometric_stations"
                :stations="watershedDetails.hydrometric_stations"/>
            </v-tab-item>

            <!-- Streamflow Report -->
            <v-tab-item>
              <StreamflowInventory
                :coordinates="this.pointOfInterest.geometry.coordinates"
              ></StreamflowInventory>
            </v-tab-item>

            <!-- Known BC Fish Observations -->
            <v-tab-item>
              <FishObservations :watershedID="selectedWatershed"/>
            </v-tab-item>

            <!-- FIDQ -->
            <v-tab-item>
              <FishInventories :watershedID="selectedWatershed"/>
            </v-tab-item>

            <!-- Comparative Runoff Models -->
            <v-tab-item>
              <WatershedAvailability :allWatersheds="watersheds"
                                     :record="selectedWatershedRecord"/>
            </v-tab-item>
          </v-tabs>
        </div>
      </div>
    </template>

    <!-- old components -->
<!--    <v-banner one-line>-->
<!--      <v-avatar-->
<!--        slot="icon"-->
<!--        color="blue accent-4"-->
<!--        size="40"-->
<!--      >-->
<!--        <v-icon-->
<!--          icon="mdi-exclamation"-->
<!--          color="white"-->
<!--        >-->
<!--          mdi-exclamation-->
<!--        </v-icon>-->
<!--      </v-avatar>-->

<!--      <p>-->
<!--        This modelling output has not been peer reviewed and is still considered-->
<!--        experimental. Use the values generated with your own discretion.-->
<!--      </p>-->

<!--    </v-banner>-->
<!--    <template v-if="watersheds && watersheds.length">-->
<!--      <v-row>-->
<!--        <v-col cols=12 md=12 class="text-right">-->
<!--          <v-btn outlined color="primary" @click="resetWatershed">Reset</v-btn>-->
<!--        </v-col>-->
<!--      </v-row>-->
<!--      <v-row align="center">-->
<!--        <v-col cols=12 md=12>-->
<!--          <v-select-->
<!--            v-model="selectedWatershed"-->
<!--            :items="watershedOptions"-->
<!--            :menu-props="{ maxHeight: '400' }"-->
<!--            label="Select watershed"-->
<!--            item-text="label"-->
<!--            item-value="value"-->
<!--            hint="Available watersheds at this location"-->
<!--          ></v-select>-->
<!--        </v-col>-->
<!--      </v-row>-->

<!--      <div v-if="selectedWatershed">-->
<!--        <div v-if="watershedDetailsLoading">-->
<!--          <v-progress-linear indeterminate show></v-progress-linear>-->
<!--        </div>-->
<!--        <div v-else>-->
<!--          <div>Watershed Details-->
<!--             <v-tooltip right v-if="this.scsb2016ModelInputs">-->
<!--                <template v-slot:activator="{ on }">-->
<!--                  <v-btn v-on="on" x-small fab depressed light-->
<!--                         @click="openEditableModelInputsDialog">-->
<!--                    <v-icon small color="primary">-->
<!--                      mdi-tune-->
<!--                    </v-icon>-->
<!--                  </v-btn>-->
<!--                </template>-->
<!--                <span>Customize Model Inputs</span>-->
<!--              </v-tooltip>-->
<!--          </div>-->

<!--          <v-alert-->
<!--            v-if="customModelInputsActive"-->
<!--            class="my-5"-->
<!--            outlined-->
<!--            type="warning"-->
<!--            prominent-->
<!--            border="left"-->
<!--          >-->
<!--            <p>-->
<!--              You are using custom model inputs and not the values supplied by the-->
<!--              Wally API.-->
<!--            </p>-->
<!--          </v-alert>-->

<!--          <v-dialog v-model="show.editingModelInputs" persistent>-->
<!--            <EditableModelInputs-->
<!--              @close="closeEditableModelInputsDialog"/>-->
<!--          </v-dialog>-->

<!--          <v-row>-->
<!--            <v-col class="text-right">-->
<!--              <v-btn outlined v-on:click="downloadWatershedInfo()"-->
<!--                     color="primary" class="mx-1">-->
<!--                <span class="hidden-sm-and-down">-->
<!--                  PDF-->
<!--                  <v-icon class="ml-1">cloud_download</v-icon>-->
<!--                  </span>-->
<!--              </v-btn>-->
<!--              <v-btn-->
<!--                  class="mx-1"-->
<!--                  outlined-->
<!--                  @click="exportWatershedXLSX"-->
<!--                  color="primary"-->
<!--                >-->
<!--                  Excel-->
<!--                  <v-icon class="ml-1" v-if="!spreadsheetLoading">-->
<!--                    cloud_download-->
<!--                  </v-icon>-->
<!--                  <v-progress-circular-->
<!--                    v-if="spreadsheetLoading"-->
<!--                    indeterminate-->
<!--                    size=24-->
<!--                    class="ml-1"-->
<!--                    color="primary"-->
<!--                  ></v-progress-circular>-->
<!--              </v-btn>-->
<!--            </v-col>-->
<!--          </v-row>-->

<!--          <div>-->
<!--            <MeanAnnualRunoff :record="selectedWatershedRecord"/>-->
<!--            <WatershedDemand :watershedID="selectedWatershed"/>-->
<!--            <ShortTermDemand :watershedID="selectedWatershed"/>-->
<!--            <AvailabilityVsDemand/>-->
<!--            <HydrometricStationsContainer-->
<!--              v-if="watershedDetails && watershedDetails.hydrometric_stations"-->
<!--              :stations="watershedDetails.hydrometric_stations"-->
<!--            class="pt-8" />-->
<!--            <StreamflowInventory-->
<!--              :coordinates="this.pointOfInterest.geometry.coordinates"-->
<!--            ></StreamflowInventory>-->
<!--            <FishObservations :watershedID="selectedWatershed"/>-->
<!--            <FishInventories :watershedID="selectedWatershed"/>-->
<!--            <WatershedAvailability :allWatersheds="watersheds"-->
<!--                                   :record="selectedWatershedRecord"/>-->
<!--          </div>-->
<!--        </div>-->
<!--      </div>-->
<!--    </template>-->
  </div>
</template>

<script>
import { mapGetters, mapMutations, mapActions } from 'vuex'
import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'
import ApiService from '../../../services/ApiService'
import qs from 'querystring'
import WatershedAvailability from './WatershedAvailability'
import MeanAnnualRunoff from './MeanAnnualRunoff'
import EditableModelInputs from './EditableModelInputs'
import HydrometricStationsContainer from './hydrometric_stations/HydrometricStationsContainer'
import FishObservations from './FishObservations'
import WatershedDemand from './watershed_demand/WatershedDemand'
import ShortTermDemand from './watershed_demand/ShortTermDemand'
import FishInventories from './fish_inventories/FishInventories'
import AvailabilityVsDemand from './watershed_demand/AvailabilityVsDemand'
import StreamflowInventory from './streamflow_inventory/StreamflowInventory'

import SurfaceWaterHeaderButtons from './SurfaceWaterHeaderButtons'
import WatershedDetails from './WatershedDetails'
import WatershedMonthlyDischarge from './WatershedMonthlyDischarge'
import WatershedLicencedQty from './watershed_demand/WatershedLicencedQty'
import WaterApprovalPoints from './watershed_demand/WaterApprovalPoints'

import { months, secondsInMonth } from '../../../constants/months'
export default {
  name: 'SurfaceWaterDetails',
  components: {
    HydrometricStationsContainer,
    WatershedAvailability,
    // MeanAnnualRunoff,
    // EditableModelInputs,
    FishObservations,
    // WatershedDemand,
    // ShortTermDemand,
    // AvailabilityVsDemand,
    FishInventories,
    StreamflowInventory,

    SurfaceWaterHeaderButtons,
    WatershedDetails,
    WatershedMonthlyDischarge,
    WatershedLicencedQty,
    // WaterApprovalPoints
  },
  data: () => ({
    tab: null,
    infoTabs: null,
    watershedLoading: false,
    selectedWatershed: null,
    assessmentWatershed: null,
    hydrometricWatershed: null,
    watersheds: [],
    geojsonLayersAdded: [],
    includePOIPolygon: false,
    watershedDetailsLoading: false,
    spreadsheetLoading: false,
    show: {
      editingModelInputs: false
    },
    modelOutputs: {
      mad: 0,
      mar: 0,
      low7q2: 0,
      dry7q10: 0,
      monthlyDischarges: [],
      monthlyDistributions: []
    }
  }),
  watch: {
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
      let props = this.selectedWatershedRecord.properties
      name = props.GNIS_NAME_1 ? props.GNIS_NAME_1
        : props.SOURCE_NAME ? props.SOURCE_NAME
          : props.name ? props.name
            : props.WATERSHED_FEATURE_ID ? props.WATERSHED_FEATURE_ID
              : props.OBJECTID ? props.OBJECTID : ''
      console.log('name')
      console.log(name)
      return name.toString()
    },
    selectedWatershedRecord () {
      if (!this.selectedWatershed || !this.watersheds) {
        return null
      }
      return this.watersheds.find((ws) => ws.id === this.selectedWatershed)
    },
    watershedOptions () {
      return this.watersheds.map((w, i) => ({
        label: (w.properties['GNIS_NAME_1'] ||
          w.properties['SOURCE_NAME'] ||
          w.properties['name'] ||
          `Watershed ${i + 1}`).toLowerCase(),
        value: w.id
      }))
    },
    ...mapGetters('surfaceWater', ['watershedDetails', 'customModelInputsActive', 'scsb2016ModelInputs']),
    ...mapGetters(['pointOfInterest']),
    ...mapGetters('map', ['map'])
  },
  methods: {
    ...mapMutations('surfaceWater', ['setAvailabilityPlotData']),
    exportWatershedXLSX () {
      // Custom metrics - Track Excel downloads
      window._paq && window._paq.push([
        'trackLink',
        `${process.env.VUE_APP_AXIOS_BASE_URL}/api/v1/watersheds/${this.selectedWatershed}`,
        'download'])

      const params = {
        format: 'xlsx'
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

        let blob = new Blob([res.data], { type:
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
        let link = document.createElement('a')
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
    downloadWatershedInfo (plotType) {
      // var elementHandler = {
      //   '#ignorePDF': function (element, renderer) {
      //     return true
      //   }
      // }
      let doc = jsPDF('p', 'in', [230, 900])
      let width = doc.internal.pageSize.getWidth()
      let height = doc.internal.pageSize.getHeight()
      let filename = 'watershed--'.concat(this.watershedName) +
        '--'.concat(new Date().toISOString()) + '.pdf'
      // doc.fromHTML(document.getElementById("watershedInfo"), 15, 0.5, { 'width': 180, 'elementHandlers': elementHandler})
      // doc.save(filename)
      html2canvas(document.getElementById('watershedInfo'))
        .then(canvas => {
          let img = canvas.toDataURL('image/png')
          const imgProps = doc.getImageProperties(img)
          let size = this.scaleImageToFit(width, height, imgProps.width,
            imgProps.height)
          doc.addImage(img, 'PNG', 0, 0, size[0], size[1])
          doc.save(filename)
        })
    },
    scaleImageToFit (ws, hs, wi, hi) {
      let ri = wi / hi
      let rs = ws / hs
      let size = rs > ri ? [wi * hs / hi, hs] : [ws, hi * ws / wi]
      return size
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
    addSingleWatershedLayer (id = 'watershedsAtLocation',
      data, color = '#039be5', opacity = 0.3) {
      this.map.addLayer({
        id: id,
        type: 'fill',
        source: {
          type: 'geojson',
          data: data
        },
        layout: {
          visibility: 'none'
        },
        paint: {
          'fill-color': color,
          'fill-outline-color': '#003366',
          'fill-opacity': opacity
        }
      }, 'water_rights_licences')
    },
    fetchWatersheds () {
      this.watershedLoading = true
      const params = {
        point: JSON.stringify(this.pointOfInterest.geometry.coordinates),
        include_self: this.includePOIPolygon
      }

      this.$router.push({
        query: { coordinates: this.pointOfInterest.geometry.coordinates }
      })

      ApiService.query(`/api/v1/watersheds/?${qs.stringify(params)}`)
        .then(r => {
          const data = r.data
          this.watersheds = data.features
          this.watersheds.forEach((ws, i) => {
            if (i === 0) this.selectedWatershed = ws.id
            this.addSingleWatershedLayer(`ws-${ws.id}`, ws)
            this.geojsonLayersAdded.push(`ws-${ws.id}`)
          })
          this.watershedLoading = false
        })
        .catch(e => {
          console.error(e)
          this.watershedLoading = false
        })
    },
    fetchWatershedDetails () {
      this.watershedDetailsLoading = true
      ApiService.query(`/api/v1/watersheds/${this.selectedWatershed}`)
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
          console.error(e)
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
        let outputs = details.scsb2016_model
        let mar = outputs.find((x) => x.output_type === 'MAR')
        let mad = outputs.find((x) => x.output_type === 'MAD' && x.month === 0)
        let low7q2 = outputs.find((x) => x.output_type === '7Q2')
        let dry7q10 = outputs.find((x) => x.output_type === 'S-7Q10')
        let monthlyDistributions = outputs.filter((x) => x.output_type === 'MD')
        let monthlyDischarges = outputs.filter((x) => x.output_type === 'MAD' && x.month !== 0)
        this.modelOutputs = {
          sourceDescription: 'Model output based on South Coast Stewardship Baseline (Sentlinger, 2016).',
          mar: mar.model_result.toFixed(2),
          mad: mad.model_result.toFixed(2),
          low7q2: low7q2.model_result.toFixed(2),
          dry7q10: dry7q10.model_result.toFixed(2),
          monthlyDistributions: monthlyDistributions,
          monthlyDischarges: monthlyDischarges
        }
        let availability = monthlyDischarges.map((m) => { return m.model_result * months[m.month] * secondsInMonth })
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
    ]),
    openEditableModelInputsDialog () {
      this.show.editingModelInputs = true
    },
    closeEditableModelInputsDialog () {
      this.show.editingModelInputs = false
    }
  },
  mounted () {
    this.setMode({ type: 'analyze', name: 'surface_water' })
    this.fetchWatersheds()
  },
  beforeDestroy () {
    this.resetGeoJSONLayers()
    this.clearWatershedDetailsAndDefaults()
    this.setMode({ type: 'interactive', name: '' })
  }
}
</script>

<style>
.v-list-item__content, .v-select__selection{
  text-transform: capitalize;
}
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
</style>
