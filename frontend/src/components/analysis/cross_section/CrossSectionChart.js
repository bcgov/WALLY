import PlotlyJS from 'plotly.js'
import { mapActions } from 'vuex'

const loadPlotly = import(/* webpackPrefetch: true */ 'vue-plotly')
// let Plotly

export default {
  name: 'CrossSectionChart',
  components: {
    Plotly: () => loadPlotly.then(module => {
      return module.Plotly
    }),
    PlotlyJS
  },
  props: [
    'wells', 'wellsLithology',
    'elevations', 'waterbodies',
    'screens', 'dataLoading'],
  data: () => ({
    plotId: '2dPlot',
    displayWaterbodyAnnotations: true,
    ignoreButtons: [
      'toImage',
      'sendDataToCloud',
      'hoverCompareCartesian',
      'hoverClosestCartesian',
      'toggleSpikelines'
    ]
  }),
  mounted () {
    this.$nextTick(() => {
      this.initPlotly()
    })
  },
  computed: {
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
    }
  },
  methods: {
    ...mapActions('map', ['removeElementsByClass']),
    initPlotly () {
      setTimeout(() => {
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
      }, 300)
    },
    resetMarkerLabels () {
      this.$refs.crossPlot.$el.removeEventListener('plotly_beforehover', () => {
        return false
      })
      this.$refs.crossPlot.$el.on('plotly_beforehover', () => {
        return true
      })
      PlotlyJS.Fx.hover(this.plotId, [])
      // reset all selection data so points gain back opacity
      this.$refs.crossPlot.data.forEach((d) => {
        d.selectedpoints = null
      })
      this.$refs.crossPlot.react()
    },
    setMarkerLabels (e) {
      if (e && e.points.length > 0) {
        // This overrides hiding the hover labels
        this.$refs.crossPlot.$el.removeEventListener('plotly_beforehover', () => {
          return true
        })
        this.$refs.crossPlot.$el.on('plotly_beforehover', () => {
          return false
        })
        // hide selection box
        this.removeElementsByClass('select-outline')
        let points = e.points.map(p => {
          return { curveNumber: p.curveNumber, pointNumber: p.pointNumber }
        })

        /*
         HACK: This hack forces the graph scale for x and y to be 1.
         This is here because plotly isn't able to set it, possibly due to a problem with vuetify.
         https://apps.nrs.gov.bc.ca/int/jira/browse/WATER-1679
         */
        const gd = document.getElementById(this.plotId)
        gd._fullLayout._invScaleX = 1
        gd._fullLayout._invScaleY = 1

        // force show labels
        PlotlyJS.Fx.hover(this.plotId, points)
      }
    }
  }
}
