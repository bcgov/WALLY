<template>
  <div>
    <v-row>
      <v-col>
        <Plotly :data="chartData" :layout="layout"></Plotly>
        <Plotly :data="testData" :layout="testLayout"></Plotly>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col>
        <v-expansion-panels class="mt-5 elevation-0" multiple>
          <v-expansion-panel class="elevation-0">
            <v-expansion-panel-header
              disable-icon-rotate
              class="grey--text text--darken-4 subtitle-1"
            >
              Where does this information come from?
              <template v-slot:actions>
                <v-icon color="primary">mdi-help-circle-outline</v-icon>
              </template>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <p>
                Data on this page comes from
                <a
                  href="https://apps.nrs.gov.bc.ca/gwells/"
                  target="_blank"
                >Groundwater Wells and Aquifers</a> and the
                <a
                  href="https://open.canada.ca/data/en/dataset/7f245e4d-76c2-4caa-951a-45d1d2051333"
                  target="_blank"
                >Canadian Digital Elevation Model</a>.
              </p>
              <dl>
                <dt>Canadian Digital Elevation Model (CDEM)</dt>
                <dd>
                  The CDEM stems from the existing Canadian Digital Elevation Data (CDED). The latter were extracted
                  from the hypsographic andhydrographic elements of the National Topographic Data Base (NTDB) at the
                  scale of 1:50 000, the Geospatial Database (GDB), various scaled positional data acquired by the
                  provinces and territories, or remotely sensed imagery. In the CDEM data, elevations can be either
                  ground or reflective surface elevations. The CDEM data covers the Canadian Landmass.
                </dd>
                <dt>Depth to water</dt>
                <dd>
                  The depth to water, as reported in the DataBC
                  <a
                    href="https://catalogue.data.gov.bc.ca/dataset/ground-water-wells"
                    target="_blank"
                  >Ground Water Wells dataset</a> (see WATER_DEPTH).
                </dd>
                <dt>Finished well depth</dt>
                <dd>The finished well depth, as reported in the well report submitted by the well driller or pump installer (in metres).</dd>
                <dt>Well elevations</dt>
                <dd>
                  Elevations for well data (depth to water, finished well depth) are calculated by subtracting
                  the reported depth below ground level from the CDEM elevation at the location of the well.
                </dd>
              </dl>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import qs from 'querystring'
import ApiService from '../../services/ApiService'
import EventBus from '../../services/EventBus'
import { Plotly } from 'vue-plotly'

export default {
  name: 'WellsCrossSection',
  components: {
    Plotly
  },
  props: ['record', 'coordinates'],
  data: () => ({
    radius: 200,
    wells: [],
    wellsLithology: [],
    elevations: [],
    loading: false
  }),
  computed: {
    layout () {
      const opts = {
        shapes: [],
        title: 'Groundwater Wells',
        width: 750,
        height: 750,
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
        }
      }

      // this.wells.forEach(w => {
      //   const rect = {
      //     type: 'rect',
      //     xref: 'x',
      //     yref: 'y',
      //     x0: w.distance_from_origin,
      //     y0: w.ground_elevation_from_dem,
      //     x1: w.distance_from_origin,
      //     y1: w.ground_elevation_from_dem - w.finished_well_depth,
      //     fillcolor: '#808080',
      //     opacity: 0.3,
      //     line: {
      //       width: 3
      //     }
      //   }
      //   console.log(rect)
      //   opts.shapes.push(rect)
      // })

      this.wellsLithology.forEach(lith => {
        const rect = {
          type: 'rect',
          xref: 'x',
          yref: 'y',
          x0: lith.x,
          y0: lith.y1,
          x1: lith.x,
          y1: lith.y0,
          opacity: 0.5,
          line: {
            color: lith.color,
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
        textposition: 'bottom center',
        hovertemplate:
          '<b>Well</b>: %{text}' + '<br>Bottom elev.: %{y:.1f} m<br>',
        type: 'scatter',
        marker: {
          color: 'rgb(252,141,98)'
        },
        name: 'Finished well depth (reported)',
        mode: 'markers'
      }

      const waterDepth = {
        x: this.wells.map(w => w.distance_from_origin),
        y: this.wells.map(w =>
          w.water_depth ? w.ground_elevation_from_dem - w.water_depth : null
        ),
        mode: 'markers',
        marker: {
          color: 'blue',
          symbol: 'triangle-down'
        },
        name: 'Depth to water (reported)',
        hovertemplate: 'Water elev.: %{y:.1f} m<br>',
        type: 'scatter'
      }

      var lithology = []
      this.wellsLithology.forEach(lith => {
        const marker = {
          x: [lith.x],
          y: [lith.y0],
          text: [lith.data],
          mode: 'markers',
          type: 'scatter',
          marker: {
            color: [lith.color]
          },
          name: '',
          hovertemplate: '%{text} %{y} m'
        }
        lithology.push(marker)
      })

      const elevProfile = {
        x: this.elevations.map(e => e.distance_from_origin),
        y: this.elevations.map(e => e.elevation),
        mode: 'lines',
        name: 'Ground elevation',
        type: 'scatter'
      }

      return [elevProfile, waterDepth, wells, ...lithology]
    },
    testData () {
      return [
      {
        z: [
          [8.83, 8.89, 8.81, 8.87, 8.9, 8.87],
          [8.89, 8.94, 8.85, 8.94, 8.96, 8.92],
          [8.84, 8.9, 8.82, 8.92, 8.93, 8.91],
          [8.79, 8.85, 8.79, 8.9, 8.94, 8.92],
          [8.79, 8.88, 8.81, 8.9, 8.95, 8.92],
          [8.8, 8.82, 8.78, 8.91, 8.94, 8.92],
          [8.75, 8.78, 8.77, 8.91, 8.95, 8.92],
          [8.8, 8.8, 8.77, 8.91, 8.95, 8.94],
          [8.74, 8.81, 8.76, 8.93, 8.98, 8.99],
          [8.89, 8.99, 8.92, 9.1, 9.13, 9.11],
          [8.97, 8.97, 8.91, 9.09, 9.11, 9.11],
          [9.04, 9.08, 9.05, 9.25, 9.28, 9.27],
          [9, 9.01, 9, 9.2, 9.23, 9.2],
          [8.99, 8.99, 8.98, 9.18, 9.2, 9.19],
          [8.93, 8.97, 8.97, 9.18, 9.2, 9.18]
        ],
        type: 'surface'
      },
      {
        x: [3, 3],
        y: [6, 6],
        z: [9, 6],
        mode: 'lines+markers',
        type: 'scatter3d',
        marker: {
          color: 'rgb(23, 190, 207)',
          size: 6
        }
      },
      {
        x: [2, 2],
        y: [6, 6],
        z: [7, 6],
        mode: 'lines+markers',
        type: 'scatter3d',
        marker: {
          color: 'rgb(23, 190, 207)',
          size: 6
        }
      }]
    },
    testLayout () {
      return {
        title: 'Test Layout',
        autosize: true,
        width: 500,
        height: 500,
        margin: {
          l: 65,
          r: 50,
          b: 65,
          t: 90
        }
      }
    }
  },
  methods: {
    fetchWellsAlongLine () {
      const params = {
        radius: parseFloat(this.radius),
        line: JSON.stringify(this.coordinates)
      }
      ApiService.query(`/api/v1/analysis/wells/section?${qs.stringify(params)}`)
        .then(r => {
          console.log(r.data)
          this.wells = r.data.wells
          this.elevations = r.data.elevation_profile
          this.showBuffer(r.data.search_area)
          let wellIds = this.wells.map(w => w.well_tag_number).join()
          this.fetchWellsLithology(wellIds)
        })
        .catch(e => {
          console.error(e)
        })
        .finally(() => {
          this.loading = false
        })
    },
    fetchWellsLithology (ids) {
      // https://gwells-dev-pr-1488.pathfinder.gov.bc.ca/gwells/api/v1/wells/lithology?wells=112316
      // ApiService.query(`/api/v1/analysis/wells/section?${qs.stringify(params)}`).then((r) => {
      // DEBUG
      // ids = '112316'
      // let result = `{"count":1,"next":null,"previous":null,"results":[{"well_tag_number":112316,"lithologydescription_set":[{"start":"0.00","end":"1.00","lithology_raw_data":"DARK BROWN TOPSOIL","lithology_colour":"brown","lithology_hardness":"Soft","lithology_observation":"DRY","water_bearing_estimated_flow":null},{"start":"1.00","end":"144.00","lithology_raw_data":"GRAVEL, FINE SAND","lithology_colour":"brown","lithology_hardness":"Medium","lithology_observation":"DRY","water_bearing_estimated_flow":null},{"start":"144.00","end":"167.00","lithology_raw_data":"GRAVEL, FINE SAND","lithology_colour":"brown","lithology_hardness":"Medium","lithology_observation":"WET","water_bearing_estimated_flow":"4.0000"},{"start":"167.00","end":"175.00","lithology_raw_data":"GRAVEL, MEDIUM SAND","lithology_colour":"rust-coloured","lithology_hardness":"Medium","lithology_observation":"WET, HIGH IRON","water_bearing_estimated_flow":"10.0000"},{"start":"175.00","end":"200.00","lithology_raw_data":"MEDIUM SAND, GRAVEL","lithology_colour":"grey","lithology_hardness":"Medium","lithology_observation":"WET","water_bearing_estimated_flow":"15.0000"}]}]}`
      // let results = JSON.parse(result).results

      // this.wellsLithology = lithologyList
      console.log(ids)

      ApiService.getRaw(`https://gwells-dev-pr-1488.pathfinder.gov.bc.ca/gwells/api/v1/wells/lithology?wells=${ids}`).then((r) => {
        console.log(r.data.results)
        let results = r.data.results
        var lithologyList = []
        for (let index = 0; index < results.length; index++) {
          const wellLithologySet = results[index]
          let well = this.wells.find(
            x => x.well_tag_number === wellLithologySet.well_tag_number
          )
          wellLithologySet.lithologydescription_set.forEach(w => {
            lithologyList.push({
              x: well.distance_from_origin,
              y0: well.ground_elevation_from_dem - (w.start * 0.3048),
              y1: well.ground_elevation_from_dem - (w.end * 0.3048),
              data: w.lithology_raw_data,
              color: w.lithology_colour,
              hardness: w.lithology_hardness,
              observation: w.lithology_observation,
              flow: w.water_bearing_estimated_flow
            })
          })
          this.wellsLithology = lithologyList
        }
      }).catch((e) => {
        console.error(e)
      }).finally(() => {
        this.loading = false
      })
    },
    showBuffer (polygon) {
      polygon.id = 'user_search_radius'

      // remove old shapes
      EventBus.$emit('shapes:reset')

      // add the new one
      EventBus.$emit('shapes:add', polygon)
    }
  },
  watch: {
    record: {
      handler () {
        this.fetchWellsAlongLine()
      },
      deep: true
    },
    radius (value) {
      this.fetchWellsAlongLine()
    }
  },
  mounted () {
    this.fetchWellsAlongLine()
  },
  beforeDestroy () {
    // reset shapes when closing this component
    EventBus.$emit('shapes:reset')
  }
}
</script>

<style>
</style>
