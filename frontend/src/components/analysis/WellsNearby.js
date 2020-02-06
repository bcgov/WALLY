import { mapGetters } from 'vuex'
import qs from 'querystring'
import ApiService from '../../services/ApiService'
import debounce from 'lodash.debounce'
import circle from '@turf/circle'
import { Plotly } from 'vue-plotly'

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
    wells: [],
    loading: false,
    headers: [
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
    ...mapGetters('map', ['isMapLayerActive'])
  },
  methods: {
    exportDrawdownAsSpreadsheet () {
      this.spreadsheetLoading = true
      const params = {
        radius: parseFloat(this.radius),
        point: JSON.stringify(this.coordinates),
        format: 'xlsx'
      }
      ApiService.query(`/api/v1/wells/nearby`, params, { responseType: 'arraybuffer' }).then((r) => {
        console.log(r)
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
    }
  },
  mounted () {
    this.fetchWells()
  },
  beforeDestroy () {
    this.$store.commit('map/removeShapes')
    this.$store.dispatch('map/clearSelections')
  }
}
