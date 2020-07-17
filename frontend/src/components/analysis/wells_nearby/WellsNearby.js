import { mapGetters, mapActions } from 'vuex'
import qs from 'querystring'
import ApiService from '../../../services/ApiService'
import debounce from 'lodash.debounce'
import circle from '@turf/circle'

import WellsNearbyBoxPlot from './WellsNearbyBoxPlot'

import { downloadXlsx } from '../../../utils/exportUtils'

const Plotly = () => import('vue-plotly').then(module => {
  return module.Plotly
})

export default {
  name: 'WellsNearby',
  components: {
    Plotly,
    WellsNearbyBoxPlot
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
    wellsByAquifer: {},
    defaultWellsByAquifer: {},
    loading: false,
    headers: [
      {
        text: '',
        value: 'delete',
        sortable: false,
        align: 'start',
        divider: true
      },
      {
        text: 'Distance (m)',
        value: 'distance',
        align: 'end',
        divider: true },
      {
        text: 'Well tag number',
        value: 'well_tag_number',
        align: 'start',
        divider: true },
      {
        text: 'Reported yield (USGPM)',
        value: 'well_yield',
        align: 'end',
        divider: true },
      {
        text: 'Static water level (ft btoc)',
        value: 'static_water_level',
        align: 'end',
        divider: true },
      {
        text: 'Top of screen (ft bgl)',
        value: 'top_of_screen',
        align: 'end',
        divider: true },
      {
        text: 'Finished well depth (ft bgl)',
        value: 'finished_well_depth',
        align: 'end',
        divider: true },
      {
        text: 'SWL to top of screen (ft)',
        value: 'swl_to_screen',
        align: 'end',
        divider: true },
      {
        text: 'SWL to bottom of well (ft)',
        value: 'swl_to_bottom_of_well',
        align: 'end',
        divider: true },
      {
        text: 'Aquifer Number',
        value: 'aquifer_id',
        align: 'center',
        divider: true },
      {
        text: 'Aquifer Lithology',
        value: 'aquifer_lithology',
        align: 'start',
        divider: true },
      {
        text: 'Aquifer Material',
        value: 'aquifer_material',
        align: 'start' }
    ]
  }),
  computed: {
    isWellsLayerEnabled () {
      return this.isMapLayerActive('groundwater_wells')
    },
    wellCount () {
      return Object.values(this.wellsByAquifer).reduce((a, b) => (a + b.length), 0)
    },
    coordinates () {
      return (this.record && this.record.geometry && this.record.geometry.coordinates) || []
    },
    wellsByAquiferIndexes () {
      return Object.entries(this.wellsByAquifer).map((entry, index) => index)
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
      let wellsExport = []

      Object.values(this.wellsByAquifer).forEach(wells => {
        wellsExport = wellsExport.concat(wells.map(w => w.well_tag_number))
      })

      const params = {
        radius: parseFloat(this.radius),
        point: JSON.stringify(this.coordinates),
        export_wells: wellsExport
      }
      ApiService.post(`/api/v1/wells/nearby/export`, params, { responseType: 'arraybuffer' }).then((r) => {
        global.config.debug && console.log('[wally]', r)
        downloadXlsx(r, 'WaterReport.xlsx')
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
      this.wellsByAquifer = []
      this.defaultWellsByAquifer = []
      this.wellRequest()
    },
    wellRequest: debounce(function () {
      this.showCircle()

      if (!this.radiusIsValid(this.radius)) {
        return
      }

      const params = {
        radius: parseFloat(this.radius),
        point: JSON.stringify(this.coordinates)
      }
      ApiService.query(`/api/v1/wells/nearby/aquifers?${qs.stringify(params)}`).then((r) => {
        this.wellsByAquifer = r.data
        this.defaultWellsByAquifer = { ...this.wellsByAquifer }
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
      // clear highlighted point
      this.$store.dispatch('map/clearHighlightLayer')

      // remove old shapes
      this.$store.commit('map/removeShapes')

      // add the new one
      this.$store.commit('map/addShape', shape)
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
    deleteWell (aquifer, selectedWell) {
      console.log(selectedWell)
      // delete selected well from well list
      let newWellsByAquifer = this.wellsByAquifer[aquifer].filter(well => {
        return well['well_tag_number'] !== selectedWell['well_tag_number']
      })

      this.wellsByAquifer[aquifer] = newWellsByAquifer
      this.$store.dispatch('map/clearHighlightLayer')
    },
    resetWells () {
      this.wellsByAquifer = this.defaultWellsByAquifer
    },
    handleRedraw () {
      this.$emit('crossSection:redraw')
    },
    onMouseEnterWellItem (well) {
      // highlight well on map that corresponds to the
      // hovered list item in the nearby wells table
      let feature = {
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
