<template>
  <div>
    <v-row>
      <v-col>
        <Plotly :data="chartData" :layout="layout"></Plotly>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col>
        <v-expansion-panels class="mt-5 elevation-0" multiple>
          <v-expansion-panel class="elevation-0">
            <v-expansion-panel-header disable-icon-rotate class="grey--text text--darken-4 subtitle-1">
              Where does this information come from?
              <template v-slot:actions>
                <v-icon color="primary">mdi-help-circle-outline</v-icon>
              </template>

            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <p>
                Data on this page comes from <a href="https://apps.nrs.gov.bc.ca/gwells/" target="_blank">Groundwater Wells and Aquifers</a> and the
                <a href="https://open.canada.ca/data/en/dataset/7f245e4d-76c2-4caa-951a-45d1d2051333" target="_blank">Canadian Digital Elevation Model</a>.
              </p>
              <dl>
                <dt>Canadian Digital Elevation Model (CDEM)</dt>
                <dd>
                  The CDEM stems from the existing Canadian Digital Elevation Data (CDED). The latter were extracted
                  from the hypsographic andhydrographic elements of the National Topographic Data Base (NTDB) at the
                  scale of 1:50 000, the Geospatial Database (GDB), various scaled positional data acquired by the
                  provinces and territories, or remotely sensed imagery. In the CDEM data, elevations can be either
                  ground or reflective surface elevations. The CDEM data covers the Canadian Landmass.</dd>
                <dt>Depth to water</dt>
                <dd>The depth to water, as reported in the DataBC <a href="https://catalogue.data.gov.bc.ca/dataset/ground-water-wells" target="_blank">Ground Water Wells dataset</a> (see WATER_DEPTH).</dd>
                <dt>Finished well depth</dt>
                <dd>The finished well depth, as reported in the well report submitted by the well driller or pump installer (in metres).</dd>
                <dt>Well elevations</dt>
                <dd>Elevations for well data (depth to water, finished well depth) are calculated by subtracting
                  the reported depth below ground level from the CDEM elevation at the location of the well.</dd>
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
    elevations: [],
    loading: false
  }),
  computed: {
    layout () {
      const opts = {
        shapes: [],
        title: 'Groundwater Wells',
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

      this.wells.forEach((w) => {
        const rect = {
          type: 'rect',
          xref: 'x',
          yref: 'y',
          x0: w.distance_from_origin,
          y0: w.ground_elevation_from_dem,
          x1: w.distance_from_origin,
          y1: w.ground_elevation_from_dem - w.finished_well_depth,
          fillcolor: '#808080',
          opacity: 0.3,
          line: {
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
        y: this.wells.map(w => w.finished_well_depth ? w.ground_elevation_from_dem - w.finished_well_depth : null),
        text: this.wells.map(w => w.well_tag_number),
        textposition: 'bottom center',
        hovertemplate: '<b>Well</b>: %{text}' +
                        '<br>Bottom elev.: %{y:.1f} m<br>',
        type: 'scatter',
        marker: {
          color: 'rgb(252,141,98)' },
        name: 'Finished well depth (reported)',
        mode: 'markers'
      }

      const waterDepth = {
        x: this.wells.map(w => w.distance_from_origin),
        y: this.wells.map(w => w.water_depth ? w.ground_elevation_from_dem - w.water_depth : null),
        mode: 'markers',
        marker: {
          color: 'blue',
          symbol: 'triangle-down' },
        name: 'Depth to water (reported)',
        hovertemplate: 'Water elev.: %{y:.1f} m<br>',
        type: 'scatter'
      }

      const elevProfile = {
        x: this.elevations.map(e => e.distance_from_origin),
        y: this.elevations.map(e => e.elevation),
        mode: 'lines',
        name: 'Ground elevation',
        type: 'scatter'
      }

      return [elevProfile, waterDepth, wells]
    }
  },
  methods: {
    fetchWellsAlongLine () {
      const params = {
        radius: parseFloat(this.radius),
        line: JSON.stringify(this.coordinates)
      }
      ApiService.query(`/api/v1/analysis/wells/section?${qs.stringify(params)}`).then((r) => {
        this.wells = r.data.wells
        this.elevations = r.data.elevation_profile
        this.showBuffer(r.data.search_area)
      }).catch((e) => {
        console.error(e)
      }).finally(() => {
        this.loading = false
      })
    },
    fetchWellsLithology(wellIds) {
      //https://apps.nrs.gov.bc.ca/gwells/api/v1/wells/lithology?wells=123,1234&limit=100
      ApiService.query(`/api/v1/analysis/wells/section?${qs.stringify(params)}`).then((r) => {
        this.wells = r.data.wells
        this.elevations = r.data.elevation_profile
        this.showBuffer(r.data.search_area)
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
