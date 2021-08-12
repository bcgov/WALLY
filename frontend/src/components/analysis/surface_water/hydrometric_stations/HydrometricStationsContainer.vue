<template>
  <v-card flat v-if="this.surface_water_design_v2">
    <v-card-title
      class="title mt-5 ml-3 mr-3 pa-1 mb-2"
      dark>
      Hydrometric Stations
    </v-card-title>
    <v-card-text v-if="stations && stations.length > 0">
      <v-expansion-panels accordion multiple hover flat
                          v-if="stations && stations.length > 0">
        <v-expansion-panel v-for="(item, i) in stations" v-bind:key="i">
          <v-expansion-panel-header :key="i">
            {{item.properties.name}}
            ({{item.id}})
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <FeatureStreamStation :record="item" />
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card-text>
    <v-card-text v-else>
      <p class="text--disabled">No hydrometric stream flow stations found in this area</p>
    </v-card-text>
  </v-card>
  <v-card flat v-else>
    <p class="title font-weight-bold">Hydrometric Stations</p>
    <v-expansion-panels accordion multiple hover flat
                        v-if="stations && stations.length > 0">
      <v-expansion-panel v-for="(item, i) in stations" v-bind:key="i">
        <v-expansion-panel-header :key="i">
          {{item.properties.name}}
          ({{item.id}})
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <FeatureStreamStation :record="item" />
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
    <p v-else class="text--disabled">No hydrometric stream flow stations found in this area</p>
  </v-card>
</template>
<script>
import mapboxgl from 'mapbox-gl'
import { mapGetters } from 'vuex'

import FeatureStreamStation from '../../../features/FeatureStreamStation'
import { findWallyLayer } from '../../../../common/utils/mapUtils'
import { SOURCE_WS_HYDAT_STATIONS } from '../../../../common/mapbox/sourcesWally'
import { featureCollection } from '../../../../common/mapbox/features'

const popup = new mapboxgl.Popup({
  closeButton: false,
  closeOnClick: false
})

export default {
  name: 'HydrometricStationsContainer',
  components: {
    FeatureStreamStation
  },
  props: ['stations', 'surface_water_design_v2'],
  data: () => ({
  }),
  computed: {
    ...mapGetters('map', ['map'])
  },
  methods: {
    addStationsLayer (data) {
      global.config.debug && console.log('stations map data')
      global.config.debug && console.log(data)

      if (this.map.getLayer(SOURCE_WS_HYDAT_STATIONS)) {
        return
      }

      let waterLicencesLayer = findWallyLayer(SOURCE_WS_HYDAT_STATIONS)(featureCollection(data))
      this.map.addLayer(waterLicencesLayer, 'water_rights_licences')

      this.map.on('mouseenter', SOURCE_WS_HYDAT_STATIONS, (e) => {
        // Change the cursor style as a UI indicator.
        this.map.getCanvas().style.cursor = 'pointer'

        let coordinates = e.features[0].geometry.coordinates.slice()
        let stationName = `${e.features[0].properties['station_number']} - ${e.features[0].properties['station_name']}`

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
              <dt>WSC Station:</dt> <dd>${stationName}</dd>
            </dl>

          `)
          .addTo(this.map)
      })

      this.map.on('mouseleave', SOURCE_WS_HYDAT_STATIONS, () => {
        this.map.getCanvas().style.cursor = ''
        popup.remove()
      })
    },
    setupStationsLayer () {
      if (this.map.getLayer(SOURCE_WS_HYDAT_STATIONS)) {
        this.map.removeLayer(SOURCE_WS_HYDAT_STATIONS)
      }
      if (this.map.getSource(SOURCE_WS_HYDAT_STATIONS)) {
        this.map.removeSource(SOURCE_WS_HYDAT_STATIONS)
      }
      this.addStationsLayer(this.stations)
    }
  },
  mounted () {
    this.setupStationsLayer()
  },
  beforeDestroy () {
    if (this.map.getLayer(SOURCE_WS_HYDAT_STATIONS)) {
      this.map.removeLayer(SOURCE_WS_HYDAT_STATIONS)
      this.map.removeSource(SOURCE_WS_HYDAT_STATIONS)
    }
  }
}
</script>
