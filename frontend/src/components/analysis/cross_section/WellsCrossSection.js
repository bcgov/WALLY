import qs from 'querystring'
import ApiService from '../../../services/ApiService'
import mapboxgl from 'mapbox-gl'
import { mapGetters, mapActions } from 'vuex'
import html2canvas from 'html2canvas'
import { saveAs } from 'file-saver'
import jsPDF from 'jspdf'
import PlotlyJS from 'plotly.js'

import CrossSectionInstructions from './CrossSectionInstructions'
import SaveAnalysisModal from '../../savedanalyses/SaveAnalysisModal'
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
    SaveAnalysisModal
  },
  mounted () {
    this.$store.commit('map/setMode',
      { type: 'analysis', name: 'cross_section' })
    this.fetchWellsAlongLine()
  },
  props: ['record', 'panelOpen'],
  data: () => ({
    radius: 200,
    wells: [],
    wellsLithology: [],
    elevations: [],
    streams: [],
    surfacePoints: [],
    selected: [],
    loading: true,
    xlsLoading: false,
    downloadImageLoading: false,
    timeout: {},
    displayWaterbodyAnnotations: true,
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
    },
    chartLayout () {
      // annotations used instead of label text due to text angle feature
      let wellAnnotations = this.wells.map((w) => {
        return {
          xref: 'x',
          yref: 'y',
          x: w.distance_from_origin,
          y: w.ground_elevation_from_dem,
          xanchor: 'left',
          yanchor: 'center',
          text: 'WTN:' + w.well_tag_number,
          textangle: -45,
          align: 'center',
          font: {
            size: 12,
            color: 'black'
          },
          opacity: 0.8,
          showarrow: true,
          standoff: 3,
          arrowhead: 1,
          arrowsize: 1,
          arrowwidth: 1,
          ax: 8,
          ay: -30
        }
      })

      // conditionally display water body annotations
      let waterbodyAnnotations = []
      if (this.displayWaterbodyAnnotations) {
        waterbodyAnnotations = this.waterbodies.map((s) => {
          return {
            xref: 'x',
            yref: 'y',
            x: s.distance,
            y: s.elevation,
            xanchor: 'left',
            yanchor: 'center',
            text: s.name,
            textangle: -45,
            align: 'center',
            font: {
              size: 12,
              color: 'black'
            },
            opacity: 0.8,
            showarrow: true,
            standoff: 3,
            arrowhead: 1,
            arrowsize: 1,
            arrowwidth: 1,
            ax: 8,
            ay: -70
          }
        })
      }

      const opts = {
        shapes: [],
        title: 'Groundwater Wells',
        height: 800,
        hovermode: 'closest',
        legend: {
          x: -0.1,
          y: 1.2
        },
        yaxis: {
          title: {
            text: 'Elevation (masl)'
          }
        },
        xaxis: {
          title: {
            text: 'Distance (m)'
          }
        },
        // start and end labls for the xsection chart
        annotations: [
          {
            xref: 'paper',
            yref: 'paper',
            x: 0,
            xanchor: 'right',
            y: -0.1,
            yanchor: 'bottom',
            text: 'A',
            showarrow: false,
            font: {
              size: 16,
              color: '#ffffff'
            },
            align: 'center',
            bordercolor: '#1A5A96',
            borderwidth: 4,
            borderpad: 4,
            bgcolor: '#1A5A96',
            opacity: 0.8
          },
          {
            xref: 'paper',
            yref: 'paper',
            x: 1,
            xanchor: 'left',
            y: -0.1,
            yanchor: 'bottom',
            text: 'B',
            showarrow: false,
            font: {
              size: 16,
              color: '#ffffff'
            },
            align: 'center',
            bordercolor: '#1A5A96',
            borderwidth: 4,
            borderpad: 4,
            bgcolor: '#1A5A96',
            opacity: 0.8
          },
          ...wellAnnotations, ...waterbodyAnnotations
        ]
      }

      this.wells.forEach(w => {
        const rect = {
          type: 'rect',
          xref: 'x',
          yref: 'y',
          x0: w.distance_from_origin,
          y0: w.ground_elevation_from_dem,
          x1: w.distance_from_origin,
          y1: w.finished_well_depth
            ? w.ground_elevation_from_dem - w.finished_well_depth
            : w.ground_elevation_from_dem,
          opacity: 0.5,
          line: {
            color: 'blue',
            width: 3
          }
        }
        opts.shapes.push(rect)
      })

      this.screens.forEach(screen => {
        // generate rectangle
        const rect = {
          type: 'rect',
          xref: 'x',
          yref: 'y',
          x0: screen.x - 3,
          y0: screen.y0,
          x1: screen.x + 3,
          y1: screen.y1,
          opacity: 0.7,
          line: {
            color: 'blue',
            width: 2
          },
          hoverlabel: {
            namelength: 0
          }
        }
        opts.shapes.push(rect)

        // generate hashmarks/lines within rectangle
        // every 0.2 metres
        Array(Math.floor(Math.abs(screen.y0 - screen.y1) * 5)).fill({}).map((item, i) => ({
          type: 'line',
          xref: 'x',
          yref: 'y',
          x0: screen.x - 3,
          y0: screen.y1 + (i + 1) * 0.2,
          x1: screen.x + 3,
          y1: screen.y1 + (i + 1) * 0.2,
          opacity: 0.7,
          line: {
            color: 'blue',
            width: 2
          }
        })).forEach(item => {
          opts.shapes.push(item)
        })
      })

      return opts
    },
    chartData () {
      const wells = {
        x: this.wells.map(w => w.distance_from_origin),
        y: this.wells.map(w =>
          w.finished_well_depth
            ? w.ground_elevation_from_dem - w.finished_well_depth
            : w.ground_elevation_from_dem
        ),
        text: this.wells.map(w => {
          return {
            fwd: w.finished_well_depth,
            dfl: w.feature.properties.distance_from_line,
            dir: w.feature.properties.compass_direction
          }
        }),
        textposition: 'bottom',
        showlegend: false,
        name: 'Finished well depth (reported)',
        hovertemplate:
          '<b>Finished Depth: </b> %{text.fwd:.2f} m' +
          '<br><b>Elevation (asl):</b> %{y:.2f} m' +
          '<br><b>Well Offset:</b> %{text.dir} %{text.dfl:.2f} m<br>',
        mode: 'markers',
        type: 'scatter',
        marker: {
          color: 'rgb(252,141,98)'
        },
        hoverlabel: {
          namelength: 0
        }
      }
      const waterDepth = {
        x: this.wells.map(w => w.distance_from_origin),
        y: this.wells.map(w =>
          w.water_depth ? w.ground_elevation_from_dem - w.water_depth : null
        ),
        mode: 'markers',
        marker: {
          color: 'blue',
          symbol: 'triangle-down',
          size: 12
        },
        name: 'Depth to water (reported)',
        hoverlabel: {
          namelength: 0
        },
        hovertemplate: 'Water elev.: %{y:.1f} m<br>',
        type: 'scatter'
      }
      const lithology = {
        x: this.wellsLithology.map(w => w.x),
        y: this.wellsLithology.map(w => w.y0),
        text: this.wellsLithology.map(w => w.data),
        mode: 'markers',
        type: 'scatter',
        textposition: 'middle right',
        marker: {
          color: this.wellsLithology.map(w => w.color)
        },
        name: 'Lithology',
        hoverlabel: {
          namelength: 0
        },
        // texttemplate: '%{text}',
        hoverinfo: 'text',
        hovertemplate: '%{text} %{y} m'
      }

      const elevProfile = {
        x: this.elevations.map(e => e.distance_from_origin),
        y: this.elevations.map(e => e.elevation),
        mode: 'lines',
        name: 'Ground elevation',
        type: 'scatter',
        showlegend: false
      }

      const streams = {
        x: this.waterbodies.map(s => s.distance),
        y: this.waterbodies.map(s => s.elevation),
        name: 'Surface water',
        text: this.waterbodies.map(s => s.name),
        textposition: 'bottom',
        mode: 'markers',
        marker: {
          color: 'white',
          symbol: 'triangle-down',
          size: 12,
          line: {
            color: 'blue',
            width: 2
          }
        }
      }

      // hover markers for screens.
      // the popup will appear at the top of the screen
      // the screens themselves are drawn using rectangles,
      // these markers only provide the popup.
      const screens = {
        x: this.screens.map(s => s.x),
        y: this.screens.map(s => s.y0),
        name: 'Screens',
        mode: 'markers',
        text: this.screens.map(s => {
          return `Screen (well ${s.well_tag_number}): ${(s.start * 0.3048).toFixed(1)} m to ${(s.end * 0.3048).toFixed(1)} m (btoc)`
        }),
        textposition: 'middle right',
        marker: {
          color: 'blue',
          symbol: 'square-cross-open',
          size: 1
        },
        showlegend: false,
        hoverlabel: {
          namelength: 0
        },
        hoverinfo: 'text',
        hovertemplate: '%{text}'
      }

      // screen icon stand-in for the rectangles that represent screens.
      // this is only to provide a legend entry.
      // null values are used to ensure that there is a legend row without any
      // data on the chart (empty arrays would result in the legend entry being omitted).
      const screensIcon = {
        x: [null],
        y: [null],
        name: 'Screens',
        mode: 'markers',
        marker: {
          color: 'blue',
          symbol: 'square-cross-open',
          size: 12
        }
      }

      return [elevProfile, waterDepth, wells, lithology, streams, screens, screensIcon]
    },
    surfaceData () {
      let lines = this.surfacePoints
      let x = []
      let y = []
      let z = []
      // build our surface points layer
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i]
        x.push(line.map(l => l[0]))
        y.push(line.map(l => l[1]))
        z.push(line.map(l => l[2]))
      }
      // add our lithology drop lines and markers
      let lithologyMarkers = []
      this.wellsLithology.forEach(lith => {
        const marker = {
          x: [lith.lon, lith.lon],
          y: [lith.lat, lith.lat],
          z: [lith.y0, lith.y1],
          text: [lith.data, lith.data],
          mode: 'lines+markers',
          type: 'scatter3d',
          showlegend: false,
          line: {
            width: 3,
            color: 'blue' // lith.color
          },
          marker: {
            size: 5,
            color: 'black' // lith.color,
          },
          hovertemplate: '%{text} %{z} m',
          // hoverinfo: 'skip',
          name: ''
        }
        lithologyMarkers.push(marker)
      })
      return [
        {
          x: x,
          y: y,
          z: z,
          type: 'surface',
          contours: {
            z: {
              show: true,
              usecolormap: true,
              highlightcolor: '#42f462',
              project: { z: true }
            }
          }
        },
        ...lithologyMarkers
      ]
    },
    surfaceLayout () {
      const emptyArr = ['', '', '']
      let a = this.surfacePoints[2][0] ? this.surfacePoints[2][0] : emptyArr
      let b = this.surfacePoints[2][0] ? this.surfacePoints[2][this.surfacePoints[2].length - 1] : emptyArr

      return {
        title: '',
        showlegend: false,
        scene: {
          xaxis: {
            title: 'Longitude'
          },
          yaxis: {
            title: 'Latitude'
          },
          zaxis: {
            title: 'Elevation (m)'
          },
          annotations: [{
            x: a[0],
            y: a[1],
            z: a[2],
            text: 'A',
            ay: -60,
            font: {
              color: 'black',
              size: 18
            }
          }, {
            x: b[0],
            y: b[1],
            z: b[2],
            text: 'B',
            ay: -60,
            font: {
              color: 'black',
              size: 18
            }
          }]
        },
        margin: {
          l: 1,
          r: 1,
          b: 1,
          t: 1
        }
      }
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
    fetchWellsAlongLine () {
      if (!this.radiusIsValid(this.radius)) {
        return
      }
      this.loading = true
      const params = {
        radius: parseFloat(this.radius),
        line: JSON.stringify(this.coordinates)
      }
      this.resetCrossSectionData()
      this.resetWellOffsetDistanceLayer()

      // Update the section line coordinates in the URL query params.
      // This enables saving/sharing links.
      if (this.coordinates.length && this.coordinates.length > 1) {
        this.$router.push({ query: {
          ...this.$route.query,
          'section_line_A': this.coordinates[0],
          'section_line_B': this.coordinates[1]
        } })
      }

      ApiService.query(`/api/v1/wells/section?${qs.stringify(params)}`)
        .then(r => {
          this.wells = r.data.wells
          this.elevations = r.data.elevation_profile
          this.surfacePoints = r.data.surface
          this.waterbodies = r.data.waterbodies
          this.screens = this.prepareScreens(r.data.wells)
          this.showBuffer(r.data.search_area)
          let wellIds = this.wells.map(w => w.well_tag_number).join()
          this.fetchWellsLithology(wellIds)
          this.addWellOffsetDistanceLayer(
            featureCollection(r.data.wells.map(x => x.feature))
          )
        })
        .catch(e => {
          console.error(e)
        })
        .finally(() => {
          this.loading = false
          this.setAnnotationMarkers()
        })
    },
    setAnnotationMarkers () {
      let annotationGeoJson = [
        {
          type: 'Feature',
          geometry: {
            type: 'Point',
            coordinates: this.coordinates[0]
          },
          properties: {
            'symbol': 'A'
          }
        },
        {
          type: 'Feature',
          geometry: {
            type: 'Point',
            coordinates: this.coordinates[1]
          },
          properties: {
            'symbol': 'B'
          }
        }
      ]
      let mapObj = this.map
      // delete any existing markers
      this.removeElementsByClass('annotationMarker')
      // add markers to map
      annotationGeoJson.forEach(function (marker) {
        // create a HTML element for each feature
        let el = document.createElement('div')
        el.className = 'annotationMarker'
        el.innerText = marker.properties.symbol

        // make a marker for each feature and add to the map
        new mapboxgl.Marker(el)
          .setLngLat(marker.geometry.coordinates)
          .addTo(mapObj)
      })
    },
    fetchWellsLithology (ids) {
      ApiService.getRaw(`https://apps.nrs.gov.bc.ca/gwells/api/v2/wells/lithology?wells=${ids}`).then((r) => {
        let results = r.data.results
        let lithologyList = []
        for (let index = 0; index < results.length; index++) {
          const wellLithologySet = results[index]
          let well = this.wells.find(
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
      }).catch((e) => {
        console.error(e)
      }).finally(() => {
        this.loading = false
        this.initPlotly()
      })
    },
    showBuffer (polygon) {
      polygon.id = 'user_search_radius'
      // remove old shapes
      this.$store.commit('map/removeShapes')
      // add the new one
      this.$store.commit('map/addShape', polygon)
    },
    initPlotly () {
      this.$nextTick(() => {
        // Subscribe to plotly select and lasso tools
        this.$refs.crossPlot.$on('selected', this.setMarkerLabels)
        this.$refs.crossPlot.$on('deselect', this.resetMarkerLabels)
        this.$refs.crossPlot.$on('relayout', this.resetMarkerLabels)
        this.$refs.crossPlot.$on('legendclick', (e) => {
          // determine whether annotations should be visible for Surface Water.
          // the `visible` field seems to show either "undefined" or "true" for when the
          // trace/data should be hidden, and `legendonly` when the data trace should be visible
          // on the plot.  This *might* have been intended to represent the "old" state before toggling...
          // todo: implement a better solution, see https://github.com/plotly/plotly.js/issues/4680
          if (e.data[e.curveNumber].name === 'Surface water') {
            if (e.data[e.curveNumber].visible !== 'legendonly') {
              this.displayWaterbodyAnnotations = false
            } else {
              this.displayWaterbodyAnnotations = true
            }
          }
        })
      })
    },
    resetMarkerLabels () {
      this.$refs.crossPlot.$el.removeEventListener('plotly_beforehover', () => { return false })
      this.$refs.crossPlot.$el.on('plotly_beforehover', () => { return true })
      PlotlyJS.Fx.hover('2dPlot', [])
      // reset all selection data so points gain back opacity
      this.$refs.crossPlot.data.forEach((d) => {
        d.selectedpoints = null
      })
      this.$refs.crossPlot.react()
    },
    setMarkerLabels (e) {
      if (e && e.points.length > 0) {
      // This overrides hiding the hover labels
        this.$refs.crossPlot.$el.removeEventListener('plotly_beforehover', () => { return true })
        this.$refs.crossPlot.$el.on('plotly_beforehover', () => { return false })
        // hide selection box
        this.removeElementsByClass('select-outline')
        let points = e.points.map(p => {
          return { curveNumber: p.curveNumber, pointNumber: p.pointNumber }
        })
        this.markerLabels = points
        PlotlyJS.Fx.hover('2dPlot', points)
      }
    },
    downloadPlotImage () {
      let filename = 'plot--'.concat(new Date().toISOString()) + '.png'
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
      let doc = jsPDF()
      let width = doc.internal.pageSize.getWidth()
      let height = doc.internal.pageSize.getHeight()
      let filename = 'plot--'.concat(new Date().toISOString()) + '.pdf'
      html2canvas(this.map._container).then(canvas1 => {
        let img1 = canvas1.toDataURL('image/png')
        const imgProps1 = doc.getImageProperties(img1)
        let size1 = this.scaleImageToFit(width, height, imgProps1.width, imgProps1.height)
        let crossDoc = jsPDF({ orientation: 'landscape', unit: 'pt', format: [size1[0], size1[1]] })
        crossDoc.addImage(img1, 'PNG', 0, 0, size1[0], size1[1])
        let plotContainer = plotType === '2d' ? this.$refs.crossPlot.$el : this.$refs.surfacePlot.$el
        html2canvas(plotContainer).then(canvas2 => {
          let img2 = canvas2.toDataURL('image/png')
          const imgProps2 = doc.getImageProperties(img2)
          let size2 = this.scaleImageToFit(width, height, imgProps2.width, imgProps2.height)
          crossDoc.addPage(size2[0], size2[1]) // add new page for next image
          crossDoc.addImage(img2, 'PNG', 0, 0, size2[0], size2[1])
          crossDoc.save(filename)
          this.downloadImageLoading = false
        })
      })
    },
    scaleImageToFit (ws, hs, wi, hi) {
      let ri = wi / hi
      let rs = ws / hs
      let size = rs > ri ? [wi * hs / hi, hs] : [ws, hi * ws / wi]
      return size
    },
    centerImage (ws, hs, hnew, wnew) {
      let w = (ws - wnew) / 2
      let h = (hs - hnew) / 2
      let pos = [w, h]
      return pos
    },
    lassoTool () {
      // layout.dragmode = 'lasso'
      // example of how to click lasso tool programatically
      Plotly.relayout('myDiv', 'dragmode', 'lasso')
    },
    radiusIsValid (val) {
      let invalid = Object.keys(this.inputRules).some((k) => {
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
      let wellsArr = this.wells.filter(well => {
        return well['well_tag_number'] !== selectedWell['well_tag_number']
      })
      // delete lithology of selected well from lithology list
      let lithologyArr = this.wellsLithology.filter(lith => {
        return lith['well_tag_number'] !== selectedWell['well_tag_number']
      })

      let screensArr = this.screens.filter(screen => {
        return screen['well_tag_number'] !== selectedWell['well_tag_number']
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

      ApiService.post(`/api/v1/wells/section/export`, params, {
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
      feature['display_data_name'] = 'groundwater_wells'
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

        let coordinates = e.features[0].geometry.coordinates.slice()
        let offsetDistance = e.features[0].properties['distance_from_line']
        let compassDirection = e.features[0].properties['compass_direction']

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
