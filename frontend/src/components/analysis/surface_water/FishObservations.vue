<template>
  <div>
    <div class="titleSub my-5">Watershed Fish Observations</div>
    <div v-if="fishLoading">
      <v-progress-linear show indeterminate></v-progress-linear>
    </div>
    <div v-if="fishData">
      <v-card flat>
        <div>
            Source:
            <a href="https://catalogue.data.gov.bc.ca/dataset/known-bc-fish-observations-and-bc-fish-distributions"
                target="_blank">Known BC Fish Observations and BC Fish Distributions (DataBC)</a>
        </div>
        <div class="my-5">
          <v-data-table
            :items="fishData.fish_species_data"
            :headers="fishObservationHeaders"
            sort-by="qty"
            sort-desc
          >
            <template v-slot:item.qty="{ item }">
              {{ item.qty.toFixed(1) | formatNumber }}
            </template>
          </v-data-table>
          <v-col class="text-right">
            <v-btn @click="toggleLayerVisibility" color="primary" outlined>{{isFishLayerVisible ? 'Hide Points' : 'Show Points'}}</v-btn>
          </v-col>
        </div>
      </v-card>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import ApiService from '../../../services/ApiService'
import mapboxgl from 'mapbox-gl'

const popup = new mapboxgl.Popup({
  closeButton: false,
  closeOnClick: false
})

export default {
  name: 'FishObservations',
  components: {
  },
  props: ['watershedID', 'record'],
  data: () => ({
    fishLoading: false,
    fishData: null,
    fishObservationHeaders: [
      { text: 'Fish Species', value: 'species', sortable: true },
      { text: 'Observation Count', value: 'count', align: 'center' },
      { text: 'Life Stages Observed', value: 'life_stages', align: 'center' },
      { text: 'First Observation Date', value: 'observation_date_min', align: 'center' },
      { text: 'Last Observation Date', value: 'observation_date_max', align: 'center' }
    ],
    isFishLayerVisible: true
  }),
  computed: {
    ...mapGetters('map', ['map'])
  },
  watch: {
    watershedID () {
      this.fishData = null
      this.map.removeLayer('fishObservations')
      this.map.removeSource('fishObservations')
      this.fetchFishObservations()
    }
  },
  methods: {
    fetchFishObservations () {
      this.fishLoading = true
      ApiService.query(`/api/v1/watersheds/${this.watershedID}/fish_observations`)
        .then(r => {
          this.fishData = r.data
          this.addFishObservationsLayer('fishObservations', r.data.fish_observations)
          this.fishLoading = false
        })
        .catch(e => {
          this.fishLoading = false
          console.error(e)
        })
    },
    addFishObservationsLayer (id = 'fishObservations', data, color = '#B22222', opacity = 0.5) {
      this.map.addLayer({
        id: id,
        type: 'circle',
        source: {
          type: 'geojson',
          data: data
        },
        paint: {
          'circle-color': color,
          'circle-radius': 5,
          'circle-opacity': opacity
        }
      }, 'fish_observations')

      this.map.on('mouseenter', id, (e) => {
      // Change the cursor style as a UI indicator.
        this.map.getCanvas().style.cursor = 'pointer'

        let coordinates = e.features[0].geometry.coordinates.slice()
        let speciesName = e.features[0].properties['SPECIES_NAME']
        let lifeStage = e.features[0].properties['LIFE_STAGE']
        let observationDate = e.features[0].properties['OBSERVATION_DATE']

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
              <dt>Species Name:</dt> <dd>${speciesName}</dd>
              <dt>Life Stage:</dt> <dd>${lifeStage && lifeStage !== 'null' ? lifeStage : 'Not Observed'}</dd>
              <dt>Observation Date::</dt> <dd>${observationDate && observationDate !== 'null' ? observationDate : ''}</dd>
            </dl>
          `)
          .addTo(this.map)
      })

      this.map.on('mouseleave', id, () => {
        this.map.getCanvas().style.cursor = ''
        popup.remove()
      })
    },
    toggleLayerVisibility () {
      this.isFishLayerVisible = !this.isFishLayerVisible  
      this.map.setLayoutProperty('fishObservations', 'visibility', this.isFishLayerVisible ? 'visible' : 'none');
      this.map.setLayoutProperty('fish_observations', 'visibility', this.isFishLayerVisible ? 'visible' : 'none');
    }
  },
  mounted () {
    this.fetchFishObservations()
  },
  beforeDestroy () {
    this.map.removeLayer('fishObservations')
    this.map.removeSource('fishObservations')
  }
}
</script>

<style>
</style>
