import { mapGetters } from 'vuex'
import qs from 'querystring'
import ApiService from '../../services/ApiService'
import debounce from 'lodash.debounce'
import circle from '@turf/circle'
import EventBus from '../../services/EventBus'
import Chart from '../charts/Chart'

export default {
  name: 'WellsNearby',
  components: {
    Chart
  },
  props: ['record'],
  data: () => ({
    inputRules: {
      required: value => !!value || 'Required',
      number: value => !Number.isNaN(parseFloat(value)) || 'Invalid number',
      max: value => value <= 10000 || 'Radius must be between 0 and 10000 m'
    },
    radius: 1000,
    wells: [],
    loading: false,
    headers: [
      { text: 'Well tag number', value: 'well_tag_number', align: 'right' },
      { text: 'Distance (m)', value: 'distance', align: 'right' },
      { text: 'Reported yield (USGPM)', value: 'well_yield', align: 'right' },
      { text: 'Static water level (ft btoc)', value: 'static_water_level', align: 'right' },
      { text: 'Top of screen (ft bgl)', value: 'top_of_screen', align: 'right' },
      { text: 'Finished well depth (ft bgl)', value: 'finished_well_depth', align: 'right' },
      { text: 'SWL to top of screen (ft)', value: 'swl_to_screen', align: 'right' },
      { text: 'SWL to bottom of well (ft)', value: 'swl_to_bottom_of_well', align: 'right' }
    ],
    boxPlotSWLData: {
      data: [],
      id: 1,
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
      id: 2,
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
      id: '3',
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
      return this.record.geometry.coordinates
    },
    ...mapGetters(['isMapLayerActive'])
  },
  methods: {
    enableWellsLayer () {
      this.$store.commit('addMapLayer', 'groundwater_wells')
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
      ApiService.query(`/api/v1/analysis/wells/nearby?${qs.stringify(params)}`).then((r) => {
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
      EventBus.$emit('shapes:reset')

      // add the new one
      EventBus.$emit('shapes:add', shape)
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
    EventBus.$emit('shapes:reset')
  }
}
