import { mapGetters, mapActions } from 'vuex'
import qs from 'querystring'
import ApiService from '../../../services/ApiService'
import debounce from 'lodash.debounce'
import circle from '@turf/circle'

const Plotly = () => import('vue-plotly').then(module => {
  return module.Plotly
})

export default {
  name: 'WellsNearby',
  components: {
    Plotly
  },
  props: ['record'],
  data: () => ({
    spreadsheetLoading: false,
    inputRules: {
      required: value => !!value || 'Required',
      number: value => !Number.isNaN(parseFloat(value)) || 'Invalid number',
      max: value => value <= 10000 || 'Radius must be between 0 and 10000 m'
    },
    radius: 1000,
    defaultWells: [],
    wells: [],
    loading: false,
    headers: [
      { text: '', value: 'delete', sortable: false, align: 'start' },
      { text: 'Distance (m)', value: 'distance' },
      { text: 'Well tag number', value: 'well_tag_number' },
      { text: 'Reported yield (USGPM)', value: 'well_yield' },
      { text: 'Static water level (ft btoc)', value: 'static_water_level' },
      { text: 'Top of screen (ft bgl)', value: 'top_of_screen' },
      { text: 'Finished well depth (ft bgl)', value: 'finished_well_depth' },
      { text: 'SWL to top of screen (ft)', value: 'swl_to_screen' },
      { text: 'SWL to bottom of well (ft)', value: 'swl_to_bottom_of_well' }
    ],
    boxPlotSWLData: {
      data: [],
      layout: {
        font: {
          family: 'BCSans, Noto Sans, Verdana, Arial'
        },
        yaxis: {
          autorange: 'reversed',
          fixedrange: true
        },
        xaxis: {
          fixedrange: true
        },
        autosize: false,
        width: 250,
        margin: { // Margins for the chart without a title
          l: 50,
          r: 50,
          b: 50,
          t: 10,
          pad: 4
        }
      }
    },
    boxPlotYieldData: {
      data: [],
      layout: {
        font: {
          family: 'BCSans, Noto Sans, Verdana, Arial'
        },
        yaxis: {
          autorange: 'reversed',
          fixedrange: true
        },
        xaxis: {
          fixedrange: true
        },
        autosize: false,
        width: 250,
        margin: { // Margins for the chart without a title
          l: 50,
          r: 50,
          b: 50,
          t: 10,
          pad: 4
        }
      }

    },
    boxPlotFinishedDepthData: {
      data: [],
      layout: {
        font: {
          family: 'BCSans, Noto Sans, Verdana, Arial'
        },
        yaxis: {
          autorange: 'reversed',
          fixedrange: true
        },
        xaxis: {
          fixedrange: true
        },
        autosize: false,
        width: 250,
        margin: { // Margins for the chart without a title
          l: 50,
          r: 50,
          b: 50,
          t: 10,
          pad: 4
        }
      }
    }
  }),
  computed: {
    isWellsLayerEnabled () {
      return this.isMapLayerActive('groundwater_wells')
    },
    coordinates () {
      return (this.record && this.record.geometry && this.record.geometry.coordinates) || []
    },
    ...mapGetters('map', ['isMapLayerActive', 'isMapReady'])
  },
  methods: {
    ...mapActions('map', ['setDrawMode']),
    selectPoint () {
      this.setDrawMode('draw_point')
    },
    exportDrawdownAsSpreadsheet () {
      // Custom metrics - Track Excel downloads
      window._paq && window._paq.push([
        'trackLink',
        `${process.env.VUE_APP_AXIOS_BASE_URL}/api/v1/wells/nearby`,
        'download'])

      this.spreadsheetLoading = true
      const params = {
        radius: parseFloat(this.radius),
        point: JSON.stringify(this.coordinates),
        export_wells: this.wells.map(w => w.well_tag_number)
      }
      ApiService.post(`/api/v1/wells/nearby/export`, params, { responseType: 'arraybuffer' }).then((r) => {
        global.config.debug && console.log('[wally]', r)
        let blob = new Blob([r.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
        let link = document.createElement('a')
        link.href = window.URL.createObjectURL(blob)
        link.download = 'WaterReport.xlsx'
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
    enableWellsLayer () {
      this.$store.dispatch('map/addMapLayer', 'groundwater_wells')
    },
    fetchWells () {
      this.loading = true
      this.wells = []
      this.defaultWells = []
      this.wellRequest()
    },
    wellRequest: debounce(function () {
      this.showCircle()
      this.boxPlotSWLData.data = []
      this.boxPlotYieldData.data = []
      this.boxPlotFinishedDepthData.data = []
      if (!this.radiusIsValid(this.radius)) {
        return
      }

      const params = {
        radius: parseFloat(this.radius),
        point: JSON.stringify(this.coordinates)
      }
      ApiService.query(`/api/v1/wells/nearby?${qs.stringify(params)}`).then((r) => {
        this.wells = r.data
        this.defaultWells = r.data
        this.populateBoxPlotData(this.wells)
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
    showCircle () {
      const options = { steps: 32, units: 'kilometers', properties: { display_data_name: 'user_search_radius' } }
      const radius = this.radius / 1000
      const shape = circle(this.coordinates, radius, options)
      shape.id = 'user_search_radius'

      // remove old shapes
      this.$store.commit('map/removeShapes')

      // add the new one
      this.$store.commit('map/addShape', shape)
    },
    populateBoxPlotData (wells) {
      let yieldY = []
      let depthY = []
      let swlY = []
      wells.forEach(well => {
        yieldY.push(Number(well.well_yield))
        depthY.push(Number(well.finished_well_depth))
        swlY.push(Number(well.static_water_level))
      })
      this.boxPlotYieldData.data.push({
        y: yieldY,
        type: 'box',
        name: 'Well Yields (USGPM)'
      })
      this.boxPlotFinishedDepthData.data.push({
        y: depthY,
        type: 'box',
        name: 'Finished Well Depth (ft bgl)'
      })
      this.boxPlotSWLData.data.push({
        y: swlY,
        type: 'box',
        name: 'Static Water Level Depth (ft)'
      })
    },
    loadFeature () {
      global.config.debug && console.log('[wally] load feature')
      // Load Point of Interest feature from query
      if ((!this.pointOfInterest || !this.pointOfInterest.geometry) && this.$route.query.coordinates) {
        const coordinates = this.$route.query.coordinates.map((x) => Number(x))

        let data = {
          coordinates: coordinates,
          layerName: 'point-of-interest'
        }

        this.$store.dispatch('map/addFeaturePOIFromCoordinates', data)
      }
    },
    deleteWell (selectedWell) {
      // delete selected well from well list
      let wellsArr = this.wells.filter(well => {
        return well['well_tag_number'] !== selectedWell['well_tag_number']
      })
      this.wells = [...wellsArr]
      this.updateBoxPlotData()
      this.$store.dispatch('map/clearHighlightLayer')
    },
    resetWells () {
      this.wells = this.defaultWells
      this.updateBoxPlotData()
    },
    updateBoxPlotData () {
      this.boxPlotSWLData.data = []
      this.boxPlotYieldData.data = []
      this.boxPlotFinishedDepthData.data = []
      this.populateBoxPlotData(this.wells)
    },
    handleRedraw () {
      this.$emit('crossSection:redraw')
    },
    onMouseEnterWellItem (well) {
      // highlight well on map that corresponds to the
      // hovered list item in the nearby wells table
      var feature = {
        'id': well.well_tag_number,
        'type': 'Feature',
        'geometry': {
          'type': 'Point',
          'coordinates': [
            well.longitude,
            well.latitude
          ]
        },
        'properties': {}
      }
      feature['display_data_name'] = 'groundwater_wells'
      this.$store.commit('map/updateHighlightFeatureData', feature)
    }
  },
  watch: {
    record: {
      handler () {
        this.fetchWells()
      },
      deep: true
    },
    radius (value) {
      this.fetchWells()
    },
    isMapReady (value) {
      if (value) {
        this.loadFeature()
      }
    }
  },
  mounted () {
    if (this.isMapReady) {
      this.loadFeature()
    }
    this.fetchWells()
  },
  beforeDestroy () {
    this.$store.commit('map/removeShapes')
    this.$store.dispatch('map/clearSelections')
  }
}
