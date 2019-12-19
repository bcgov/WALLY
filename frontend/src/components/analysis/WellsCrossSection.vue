<template>
  <div>
    <v-row>
      <v-col>
        <v-tabs>
          <v-tabs-slider></v-tabs-slider>
          <v-tab>2D Cross Section</v-tab>
          <v-tab>3D Surface Section</v-tab>
          <v-tab-item>
            <v-card flat>
              <Plotly :data="chartData" :layout="chartLayout"></Plotly>
            </v-card>
          </v-tab-item>
          <v-tab-item>
            <v-card flat>
              <Plotly :data="surfaceData" :layout="surfaceLayout"></Plotly>
            </v-card>
          </v-tab-item>
        </v-tabs>
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
    surfacePoints: [],
    loading: false
  }),
  computed: {
    chartLayout () {
      const opts = {
        shapes: [],
        title: 'Groundwater Wells',
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
          showlegend: false,
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
    surfaceData () {
      var lines = this.surfacePoints

      var x = []
      var y = []
      var z = []
      // build our surface points layer
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        x.push(line.map(l => l[0]))
        y.push(line.map(l => l[1]))
        z.push(line.map(l => l[2]))
      }

      // add our lithology drop lines and markers
      var lithologyMarkers = []
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
            color: 'blue', //lith.color
          },
          marker: {
            size: 5,
            color: 'black' //lith.color,
          },
          hovertemplate: '%{text} %{y} m',
          name: '',
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
              show:true,
              usecolormap: true,
              highlightcolor:"#42f462",
              project:{z: true}
            }
          }
        },
        ...lithologyMarkers
      ]
    },
    surfaceLayout () {
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
          }
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
        })
    },
    fetchWellsLithology (ids) {
      // https://gwells-dev-pr-1488.pathfinder.gov.bc.ca/gwells/api/v1/wells/lithology?wells=112316
      // ApiService.query(`/api/v1/analysis/wells/section?${qs.stringify(params)}`).then((r) => {
      // DEBUG
      // ids = '112316'
      // let result = `{"count":2,"next":null,"previous":null,"results":[{"well_tag_number":72177,"latitude":50.146298,"longitude":-122.953464,"lithologydescription_set":[{"start":"0.00","end":"8.00","lithology_raw_data":"COURSE GRAVEL SOME BOULDERS","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"8.00","end":"17.00","lithology_raw_data":"WATER BEARING GRAVEL SOME SMALL BOULDERS","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"17.00","end":"26.00","lithology_raw_data":"DIRTY WATER BEARING SAND & GRAVEL","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"26.00","end":"71.00","lithology_raw_data":"dirty silty water-bearing sand & gravel, some wood","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"71.00","end":"77.00","lithology_raw_data":"VERY SILTY FINE SAND CLAY & WOOD","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"77.00","end":"86.00","lithology_raw_data":"dirty silty water-bearing sand and layers of clay, some gravel","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"86.00","end":"92.00","lithology_raw_data":"very silty fine water-bearing sand & layers of clay","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"92.00","end":"172.00","lithology_raw_data":"GRAY CLAY WITH LAYERS OF SILT","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"172.00","end":"180.00","lithology_raw_data":"VERY COURSE SHARP WATER BEARING GRAVEL","lithology_observation":null,"water_bearing_estimated_flow":null}]},{"well_tag_number":80581,"latitude":50.143818,"longitude":-122.959162,"lithologydescription_set":[{"start":"0.00","end":"4.00","lithology_raw_data":"brown sand and fill containing stones","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"4.00","end":"9.00","lithology_raw_data":"brown silty sandy soil containing wood, peat and stones","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"9.00","end":"14.00","lithology_raw_data":"grey clay","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"14.00","end":"30.00","lithology_raw_data":"grey compact silt containing wood","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"30.00","end":"34.00","lithology_raw_data":"peat and wood with some grey silt","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"34.00","end":"48.00","lithology_raw_data":"grey silt containing peat and wood","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"48.00","end":"52.00","lithology_raw_data":"grey silt with traces of peat seams and some wood","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"52.00","end":"74.00","lithology_raw_data":"darker grey silt","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"74.00","end":"81.00","lithology_raw_data":"brown firm silt containing seams of brown sand and stones, water-bearing","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"81.00","end":"116.00","lithology_raw_data":"grey with seams of stones and sand and some wood below 92'","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"116.00","end":"117.00","lithology_raw_data":"fine compact silty sand, fairly tight","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"117.00","end":"134.00","lithology_raw_data":"grey silt with seams of compact silty fine sand & containing wood from 117' to 127'","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"134.00","end":"136.00","lithology_raw_data":"grey, silty coarse gravel, sharp, silty wash","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"136.00","end":"139.00","lithology_raw_data":"grey silty coarse sand and broken coarse gravel","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"139.00","end":"142.00","lithology_raw_data":"grey compact silt, broken gravel & cobbles, sharp and tight","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"142.00","end":"145.00","lithology_raw_data":"large broken rock, yielding more water","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"145.00","end":"147.00","lithology_raw_data":"green broken rock, very tight","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"147.00","end":"158.00","lithology_raw_data":"broken grey and brown-coloured rock","lithology_observation":null,"water_bearing_estimated_flow":null},{"start":"158.00","end":"164.00","lithology_raw_data":"solid bedrock","lithology_observation":null,"water_bearing_estimated_flow":null}]}]}`
      // let resultObj = JSON.parse(result)
      // let results = resultObj.results

      // this.wellsLithology = lithologyList
      // console.log(ids)

      ApiService.getRaw(`https://gwells-staging.pathfinder.gov.bc.ca/gwells/api/v1/wells/lithology?wells=${ids}`).then((r) => {
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
              lat: wellLithologySet.latitude,
              lon: wellLithologySet.longitude,
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
