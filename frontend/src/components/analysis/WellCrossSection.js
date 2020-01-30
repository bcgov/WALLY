import qs from 'querystring'
import ApiService from '../../services/ApiService'
import { Plotly } from 'vue-plotly'
import PlotlyJS from 'plotly.js'
import mapboxgl from 'mapbox-gl'
import { mapGetters, mapActions } from 'vuex'
import html2canvas from 'html2canvas'
import { saveAs } from 'file-saver'
import jsPDF from 'jspdf'

export default {
  name: 'WellsCrossSection',
  components: {
    Plotly
  },
  mounted () {
    this.$store.commit('map/setMode',
      { type: 'analysis', name: 'cross_section' })
    this.fetchWellsAlongLine()
  },
  props: ['record', 'coordinates', 'panelOpen'],
  data: () => ({
    radius: 200,
    wells: [],
    wellsLithology: [],
    elevations: [],
    surfacePoints: [],
    selected: [],
    loading: true,
    timeout: {},
    ignoreButtons: [
      'toImage',
      'sendDataToCloud',
      'hoverCompareCartesian',
      'hoverClosestCartesian',
      'toggleSpikelines'
    ],
    headers: [
      { text: 'Well Tag No.', value: 'well_tag_number', align: 'center' },
      { text: 'Depth drilled (m)', value: 'finished_well_depth', align: 'center' },
      { text: 'Water depth (m)', value: 'water_depth', align: 'center' },
      { text: '', value: 'action', sortable: false }
    ],
    inputRules: {
      required: value => !!value || 'Required',
      number: value => !Number.isNaN(parseFloat(value)) || 'Invalid number',
      max: value => value <= 1000 || 'Radius must be between 0 and 1000 m'
    }
  }),
  computed: {
    chartLayout () {
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
        annotations: [{
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
        }, {
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
        }]
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
            : null,
          opacity: 0.5,
          line: {
            color: 'blue',
            width: 3
          }
        }
        opts.shapes.push(rect)
      })
      return opts
    },
    chartData () {
      const wells = {
        x: this.wells.map(w => w.distance_from_origin),
        y: this.wells.map(w =>
          w.finished_well_depth
            ? w.ground_elevation_from_dem - w.finished_well_depth
            : null
        ),
        text: this.wells.map(w => w.well_tag_number),
        textposition: 'bottom',
        showlegend: false,
        name: 'Finished well depth (reported)',
        hovertemplate:
          '<b>Well</b>: %{text}' + '<br>Bottom elev.: %{y:.1f} m<br>',
        mode: 'markers',
        type: 'scatter',
        marker: {
          color: 'rgb(252,141,98)'
        },
        hoverlabel: {
          namelength: 0
        }
      }
      const wellTops = {
        x: this.wells.map(w => w.distance_from_origin),
        y: this.wells.map(w => w.ground_elevation_from_dem),
        text: this.wells.map(w => 'WTN:' + w.well_tag_number),
        textposition: 'top',
        showlegend: false,
        name: '',
        mode: 'markers+text',
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
      // order wells by distance from orgin so water levels connect linearly
      let orderedWells = this.wells.sort(function (a, b) {
        return parseFloat(a.distance_from_origin) - parseFloat(b.distance_from_origin)
      })
      const waterLevel = {
        x: orderedWells.map(w => w.distance_from_origin ? w.distance_from_origin : null),
        y: orderedWells.map(w => w.water_depth ? w.ground_elevation_from_dem - w.water_depth : null),
        mode: 'lines',
        name: 'Water Level',
        line: {
          color: 'blue',
          width: 2
        },
        hoverlabel: {
          namelength: 0
        },
        hoverinfo: 'none'
      }
      return [elevProfile, wellTops, waterDepth, wells, lithology, waterLevel]
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
    ...mapGetters('map', [
      'map'
    ]),
    ...mapActions('map', [
      'removeElementsByClass'
    ]),
    fetchWellsAlongLine () {
      if (!this.radiusIsValid(this.radius)) {
        return
      }

      this.loading = true
      const params = {
        radius: parseFloat(this.radius),
        line: JSON.stringify(this.coordinates)
      }
      ApiService.query(`/api/v1/wells/section?${qs.stringify(params)}`)
        .then(r => {
          console.log(r.data)
          this.wells = r.data.wells
          this.elevations = r.data.elevation_profile
          this.surfacePoints = r.data.surface
          this.showBuffer(r.data.search_area)
          let wellIds = this.wells.map(w => w.well_tag_number).join()
          this.fetchWellsLithology(wellIds)
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
      let mapObj = this.map()
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
        console.log(r.data.results)
        let results = r.data.results
        let lithologyList = []
        for (let index = 0; index < results.length; index++) {
          const wellLithologySet = results[index]
          let well = this.wells.find(
            x => x.well_tag_number === wellLithologySet.well_tag_number
          )
          if (well) {
            wellLithologySet.lithologydescription_set.forEach(w => {
              lithologyList.push({
                well_tag_number: wellLithologySet.well_tag_number,
                x: well.distance_from_origin ? well.distance_from_origin : 0,
                y0: well.ground_elevation_from_dem - (w.start * 0.3048),
                y1: well.ground_elevation_from_dem - (w.end * 0.3048),
                lat: wellLithologySet.latitude,
                lon: wellLithologySet.longitude,
                data: w.lithology_raw_data,
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
      // Subscribe to plotly select and lasso tools
      this.$refs.crossPlot.$on('selected', this.setMarkerLabels)
      this.$refs.crossPlot.$on('deselect', this.resetMarkerLabels)
      this.$refs.crossPlot.$on('relayout', this.resetMarkerLabels)
    },
    resetMarkerLabels () {
      this.$refs.crossPlot.$el.removeEventListener('plotly_beforehover')
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
        this.$refs.crossPlot.$el.removeEventListener('plotly_beforehover')
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
      let doc = jsPDF()
      let width = doc.internal.pageSize.getWidth()
      let height = doc.internal.pageSize.getHeight()
      let filename = 'plot--'.concat(new Date().toISOString()) + '.pdf'
      html2canvas(this.map()._container).then(canvas1 => {
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
    deleteWell (selectedWell) {
      // delete selected well from well list
      let wellsArr = this.wells.filter(well => {
        return well['well_tag_number'] !== selectedWell['well_tag_number']
      })
      // delete lithology of selected well from lithology list
      let lithologyArr = this.wellsLithology.filter(lith => {
        return lith['well_tag_number'] !== selectedWell['well_tag_number']
      })
      this.wells = [...wellsArr]
      this.wellsLithology = [...lithologyArr]
    },
    highlightWell (selected) {
      // Placeholder
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
        this.fetchWellsAlongLine()
      },
      deep: true
    },
    radius (value) {
      // delay call to re-fetch data if user still inputting radius numbers
      clearTimeout(this.timeout)
      this.timeout = setTimeout(() => {
        this.fetchWellsAlongLine()
      }, 750)
    }
  },
  beforeDestroy () {
    // reset shapes when closing this component
    this.$store.commit('map/removeShapes')
    this.$store.commit('map/resetMode')
  }
}
