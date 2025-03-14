import qs from 'querystring'
import ApiService from '../../../services/ApiService'
import mapboxgl from 'mapbox-gl'
import { mapGetters, mapActions } from 'vuex'
import html2canvas from 'html2canvas'
import { saveAs } from 'file-saver'
import jsPDF from 'jspdf'
import PlotlyJS from 'plotly.js'

import CrossSectionInstructions from './CrossSectionInstructions'
import SavedAnalysesCreateModal from '../../savedanalyses/SavedAnalysesCreateModal'
import CrossSectionChart from './CrossSectionChart.vue'
import CrossSectionChart3d from './CrossSectionChart3d.vue'

import { downloadXlsx } from '../../../common/utils/exportUtils'
import { SOURCE_WELL_OFFSET_DISTANCE } from '../../../common/mapbox/sourcesWally'
import { addMapboxLayer } from '../../../common/utils/mapUtils'
import { featureCollection, geojsonFC } from '../../../common/mapbox/features'

const loadPlotly = import(/* webpackPrefetch: true */ 'vue-plotly')
let Plotly

const popup = new mapboxgl.Popup({
  closeButton: false,
  closeOnClick: false
})

export default {
  name: 'WellsCrossSection',
  components: {
    Plotly: () => loadPlotly.then(module => {
      return module.Plotly
    }),
    PlotlyJS,
    CrossSectionInstructions,
    SavedAnalysesCreateModal,
    CrossSectionChart,
    CrossSectionChart3d
  },
  mounted () {
    this.$store.commit('map/setMode',
      { type: 'analysis', name: 'cross_section' })
    // this.fetchWellsAlongLine().then().catch()
    this.fetchWellsAlongLine()
  },
  props: ['record', 'panelOpen'],
  data: () => ({
    radius: 200,
    wells: [],
    wellsLithology: [],
    waterbodies: [],
    screens: [],
    elevations: [],
    streams: [],
    surfacePoints: [],
    selected: [],
    loading: true,
    xlsLoading: false,
    downloadImageLoading: false,
    timeout: {},
    ignoreButtons: [
      'toImage',
      'sendDataToCloud',
      'hoverCompareCartesian',
      'hoverClosestCartesian',
      'toggleSpikelines'
    ],
    headers: [
      { text: 'Well Tag No.', value: 'well_tag_number', align: 'start', divider: true },
      { text: 'Depth drilled (m)', value: 'finished_well_depth', align: 'end', divider: true },
      { text: 'Water depth (m)', value: 'water_depth', align: 'end', divider: true },
      { text: 'Aquifer Number', value: 'aquifer.aquifer_id', align: 'center', divider: true },
      { text: 'Aquifer Lithology', value: 'aquifer_lithology', align: 'start', divider: true },
      { text: 'Aquifer Material', value: 'aquifer.material_desc', align: 'start', divider: true },
      { text: '', value: 'action', sortable: false }
    ],
    inputRules: {
      required: value => !!value || 'Required',
      number: value => !Number.isNaN(parseFloat(value)) || 'Invalid number',
      max: value => value <= 1000 || 'Radius must be between 0 and 1000 m'
    }
  }),
  computed: {
    ...mapGetters('map', ['map']),
    coordinates () {
      return this.record && this.record.geometry && this.record.geometry.coordinates
    }
  },
  methods: {
    ...mapGetters('map', ['isMapReady']),
    ...mapActions('map', ['removeElementsByClass']),
    handleRedraw () {
      this.$emit('crossSection:redraw')
    },
    prepareScreens (wells) {
      // creates a list of screens with a start and end height.
      // used to create rectangles on the plot indicating where screens are.
      return wells.map(w => {
        if (!w.screen_set || !w.screen_set.length) {
          return []
        }

        return w.screen_set.map(s => {
          return {
            well_tag_number: w.well_tag_number,
            x: w.distance_from_origin ? w.distance_from_origin : 0,
            y0: w.ground_elevation_from_dem - (s.start * 0.3048),
            y1: w.ground_elevation_from_dem - (s.end * 0.3048),
            ...s
          }
        })
      }).flat()
    },
    async fetchWellsAlongLine () {
      if (!this.radiusIsValid(this.radius)) {
        return
      }
      this.loading = true
      const params = {
        radius: parseFloat(this.radius),
        line: JSON.stringify(this.coordinates)
      }

      // Errors out when not contained
      // When these values get reset, an `emit` error shows up, not quite sure why
      if (this.wells.length > 0 || this.wellsLithology.length > 0 || this.screens.length > 0) {
        this.resetCrossSectionData()
      }
      this.resetWellOffsetDistanceLayer()

      // Update the section line coordinates in the URL query params.
      // This enables saving/sharing links.
      if (this.coordinates.length && this.coordinates.length > 1) {
        this.$router.push({
          query: {
            ...this.$route.query,
            section_line_A: this.coordinates[0],
            section_line_B: this.coordinates[1]
          }
        }).catch((e) => {})
      }

      // Fetch wells
      let wells = {}
      try {
        wells = await this.fetchWells(params)
      } catch (e) {
        console.error(e)
      }
      // Errors out if not contained
      // UnhandledPromiseRejection, TypeError: Cannot read property 'wells' of undefined
      if (wells && wells.data) {
        this.processWellResults(wells.data)
        this.setAnnotationMarkers()

        // Fetch Lithology
        const wellIds = this.wells.map(w => w.well_tag_number).join()
        let lithologyResults = {}
        try {
          lithologyResults = await this.fetchWellsLithology(wellIds)
        } catch (e) {
          console.error(e)
        }
        const lithology = lithologyResults.data.results
        this.buildLithologyList(lithology)

        this.loading = false
        // this.$nextTick(() => {
        //   this.initPlotly()
        // })
      }
    },
    fetchWells (params) {
      return ApiService.query(`/api/v1/wells/section?${qs.stringify(params)}`)
    },
    processWellResults (data) {
      if (!data.wells || !data.elevation_profile || !data.surface || !data.waterbodies || !data.search_area) {
        return
      }
      this.wells = data.wells
      this.elevations = data.elevation_profile
      this.surfacePoints = data.surface
      this.waterbodies = data.waterbodies
      this.screens = this.prepareScreens(data.wells)
      this.showBuffer(data.search_area)
      this.addWellOffsetDistanceLayer(
        featureCollection(data.wells.map(x => x.feature))
      )
    },
    setAnnotationMarkers () {
      const annotationGeoJson = [
        {
          type: 'Feature',
          geometry: {
            type: 'Point',
            coordinates: this.coordinates[0]
          },
          properties: {
            symbol: 'A'
          }
        },
        {
          type: 'Feature',
          geometry: {
            type: 'Point',
            coordinates: this.coordinates[1]
          },
          properties: {
            symbol: 'B'
          }
        }
      ]
      const mapObj = this.map
      // delete any existing markers
      this.removeElementsByClass('annotationMarker')
      // add markers to map
      annotationGeoJson.forEach(function (marker) {
        // create a HTML element for each feature
        const el = document.createElement('div')
        el.className = 'annotationMarker'
        el.innerText = marker.properties.symbol

        // make a marker for each feature and add to the map
        new mapboxgl.Marker(el)
          .setLngLat(marker.geometry.coordinates)
          .addTo(mapObj)
      })
    },
    fetchWellsLithology (ids) {
      return ApiService.getRaw(`https://apps.nrs.gov.bc.ca/gwells/api/v2/wells/lithology?wells=${ids}`)
    },
    buildLithologyList (results) {
      const lithologyList = []
      for (let index = 0; index < results.length; index++) {
        const wellLithologySet = results[index]
        const well = this.wells.find(
          x => x.well_tag_number === wellLithologySet.well_tag_number
        )
        if (well) {
          wellLithologySet.lithologydescription_set.forEach(w => {
          // combine lithology_raw_data and lithology_observation
            const description = [w.lithology_raw_data, w.lithology_observation].filter(Boolean).join('; ')

            lithologyList.push({
              well_tag_number: wellLithologySet.well_tag_number,
              x: well.distance_from_origin ? well.distance_from_origin : 0,
              y0: well.ground_elevation_from_dem - (w.start * 0.3048),
              y1: well.ground_elevation_from_dem - (w.end * 0.3048),
              lat: wellLithologySet.latitude,
              lon: wellLithologySet.longitude,
              data: description,
              color: w.lithology_colour,
              hardness: w.lithology_hardness,
              observation: w.lithology_observation,
              flow: w.water_bearing_estimated_flow
            })
          })
        }
      }
      this.wellsLithology = lithologyList
    },
    showBuffer (polygon) {
      polygon.id = 'user_search_radius'
      // remove old shapes
      this.$store.commit('map/removeShapes')
      // add the new one
      this.$store.commit('map/addShape', polygon)
    },
    downloadPlotImage () {
      const filename = 'plot--'.concat(new Date().toISOString()) + '.png'
      html2canvas(this.$refs.crossPlot.$el).then(canvas => {
        canvas.toBlob(function (blob) {
          saveAs(blob, filename)
        })
      })
    },
    downloadMergedImage (plotType) {
      this.downloadImageLoading = true
      // Custom Metrics - Screen capture
      window._paq && window._paq.push(['trackEvent', 'Cross Section', 'Download Plot', 'Plot pdf'])
      const doc = jsPDF()
      const width = doc.internal.pageSize.getWidth()
      const height = doc.internal.pageSize.getHeight()
      const filename = 'plot--'.concat(new Date().toISOString()) + '.pdf'
      html2canvas(this.map._container).then(canvas1 => {
        const img1 = canvas1.toDataURL('image/png')
        const imgProps1 = doc.getImageProperties(img1)
        const size1 = this.scaleImageToFit(width, height, imgProps1.width, imgProps1.height)
        const crossDoc = jsPDF({ orientation: 'landscape', unit: 'pt', format: [size1[0], size1[1]] })
        crossDoc.addImage(img1, 'PNG', 0, 0, size1[0], size1[1])
        const plotContainer = plotType === '2d' ? document.getElementById('2dPlot') : document.getElementById('3dPlot')

        html2canvas(plotContainer).then(canvas2 => {
          const img2 = canvas2.toDataURL('image/png')
          const imgProps2 = doc.getImageProperties(img2)
          const size2 = this.scaleImageToFit(width, height, imgProps2.width, imgProps2.height)
          crossDoc.addPage([size2[0], size2[1]]) // add new page for next image
          crossDoc.addImage(img2, 'PNG', 0, 0, size2[0], size2[1])
          crossDoc.save(filename)
          this.downloadImageLoading = false
        })
      })
    },
    scaleImageToFit (ws, hs, wi, hi) {
      const ri = wi / hi
      const rs = ws / hs
      const size = rs > ri ? [wi * hs / hi, hs] : [ws, hi * ws / wi]
      return size
    },
    centerImage (ws, hs, hnew, wnew) {
      const w = (ws - wnew) / 2
      const h = (hs - hnew) / 2
      const pos = [w, h]
      return pos
    },
    lassoTool () {
      // layout.dragmode = 'lasso'
      // example of how to click lasso tool programatically
      Plotly.relayout('myDiv', 'dragmode', 'lasso')
    },
    radiusIsValid (val) {
      const invalid = Object.keys(this.inputRules).some((k) => {
        return this.inputRules[k](val) !== true
      })
      return !invalid
    },
    resetCrossSectionData () {
      this.wells = []
      this.wellsLithology = []
      this.screens = []
    },
    deleteWell (selectedWell) {
      if (!this.isMapReady()) {
        return
      }
      // delete selected well from well list
      const wellsArr = this.wells.filter(well => {
        return well.well_tag_number !== selectedWell.well_tag_number
      })
      // delete lithology of selected well from lithology list
      const lithologyArr = this.wellsLithology.filter(lith => {
        return lith.well_tag_number !== selectedWell.well_tag_number
      })

      const screensArr = this.screens.filter(screen => {
        return screen.well_tag_number !== selectedWell.well_tag_number
      })

      this.wells = [...wellsArr]
      this.wellsLithology = [...lithologyArr]
      this.screens = [...screensArr]
      this.$store.dispatch('map/clearHighlightLayer')
    },
    getCrossSectionExport () {
      // Track cross section excel downloads
      window._paq && window._paq.push([
        'trackLink',
        `${global.config.baseUrl}/api/v1/wells/section/export`,
        'download'])

      const params = {
        wells: this.wells.map(w => w.well_tag_number),
        coordinates: this.coordinates,
        buffer: this.radius
      }

      this.xlsLoading = true

      ApiService.post('/api/v1/wells/section/export', params, {
        responseType: 'arraybuffer'
      }).then((res) => {
        // default filename, and inspect response header Content-Disposition
        // for a more specific filename (if provided).
        downloadXlsx(res, 'WellsCrossSection.xlsx')
        this.xlsLoading = false
      }).catch((error) => {
        console.error(error)
        this.xlsLoading = false
      })
    },
    onMouseEnterWellItem (well) {
      // highlight well on map that corresponds to the
      // hovered list item in the cross section table
      const feature = well.feature
      feature.display_data_name = 'groundwater_wells'
      this.$store.commit('map/updateHighlightFeatureData', feature)
    },
    addWellOffsetDistanceLayer (data) {
      if (this.map.getLayer(SOURCE_WELL_OFFSET_DISTANCE)) {
        return
      }
      this.map.addSource(SOURCE_WELL_OFFSET_DISTANCE, geojsonFC(data))
      addMapboxLayer(this.map, SOURCE_WELL_OFFSET_DISTANCE, {})

      this.map.on('mouseenter', SOURCE_WELL_OFFSET_DISTANCE, (e) => {
        // Change the cursor style as a UI indicator.
        this.map.getCanvas().style.cursor = 'pointer'

        const coordinates = e.features[0].geometry.coordinates.slice()
        const offsetDistance = e.features[0].properties.distance_from_line
        const compassDirection = e.features[0].properties.compass_direction

        // Ensure that if the map is zoomed out such that multiple
        // copies of the feature are visible, the popup appears
        // over the copy being pointed to.
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
          coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360
        }

        // Populate the popup and set its coordinates
        // based on the feature found.
        popup
          .setLngLat(coordinates)
          .setHTML(`
            <dl>
              <dt>Well Offset</dt> <dd>${compassDirection} ${offsetDistance.toFixed(2)} m</dd>
            </dl>
          `)
          .addTo(this.map)
      })

      this.map.on('mouseleave', SOURCE_WELL_OFFSET_DISTANCE, () => {
        this.map.getCanvas().style.cursor = ''
        popup.remove()
      })
    },
    resetWellOffsetDistanceLayer () {
      if (this.map.getLayer('wellOffsetDistance')) {
        this.map.removeLayer('wellOffsetDistance')
      }
      if (this.map.getSource('wellOffsetDistance')) {
        this.map.removeSource('wellOffsetDistance')
      }
    }
  },
  watch: {
    panelOpen (value) {
      if (value) {
        this.$store.dispatch('map/addMapLayer', 'groundwater_wells')
        this.setAnnotationMarkers()
      } else {
        this.removeElementsByClass('annotationMarker')
      }
    },
    record: {
      handler () {
        if (this.isMapReady()) {
          this.fetchWellsAlongLine()
        }
      },
      deep: true
    },
    radius (value) {
      // delay call to re-fetch data if user still inputting radius numbers
      clearTimeout(this.timeout)
      this.timeout = setTimeout(() => {
        this.fetchWellsAlongLine()
      }, 750)
    },
    isMapReady (value) {
      if (value) {
        // this.getWaterApprovals()
        this.fetchWellsAlongLine()
      }
    }
  },
  beforeDestroy () {
    // reset shapes when closing this component
    this.$store.commit('map/resetMode')
    this.$store.dispatch('map/clearSelections')
    this.$store.commit('resetSectionLine')
    this.resetWellOffsetDistanceLayer()
  }
}
