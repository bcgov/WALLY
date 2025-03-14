import PlotlyJS from 'plotly.js'

const loadPlotly = import(/* webpackPrefetch: true */ 'vue-plotly')
// let Plotly

export default {
  name: 'CrossSectionChart3d',
  components: {
    Plotly: () => loadPlotly.then(module => {
      return module.Plotly
    }),
    PlotlyJS
  },
  props: [
    'surfacePoints',
    'wellsLithology',
    'dataLoading'
  ],
  mounted () {
  },
  computed: {
    surfaceData () {
      // this.surfacePoints
      // this.wellsLithology
      const lines = this.surfacePoints
      const x = []
      const y = []
      const z = []
      // build our surface points layer
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i]
        x.push(line.map(l => l[0]))
        y.push(line.map(l => l[1]))
        z.push(line.map(l => l[2]))
      }
      // add our lithology drop lines and markers
      const lithologyMarkers = []
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
          x,
          y,
          z,
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
      const a = (this.surfacePoints[2] && this.surfacePoints[2][0]) ? this.surfacePoints[2][0] : emptyArr
      const b = (this.surfacePoints[2] && this.surfacePoints[2][0]) ? this.surfacePoints[2][this.surfacePoints[2].length - 1] : emptyArr

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
  }
}
