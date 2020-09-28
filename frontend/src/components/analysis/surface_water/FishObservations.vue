<template>
  <v-card v-if="this.surface_water_design_v2" flat>
    <v-card-title
      class="title mt-5 ml-3 mr-3 pa-1 mb-2"
      dark>
      Watershed Fish Observations
    </v-card-title>
    <v-card-actions>
      <v-card-subtitle class="pr-0 pl-2 pr-2">
        Source:
      </v-card-subtitle>
      <a href="https://catalogue.data.gov.bc.ca/dataset/known-bc-fish-observations-and-bc-fish-distributions"
         target="_blank"
         rel="external noopener">
        Known BC Fish Observations and BC Fish Distributions (DataBC)
      </a>
    </v-card-actions>
    <v-card-text v-if="fishLoading">
      <v-progress-linear show indeterminate></v-progress-linear>
    </v-card-text>
    <v-card-text v-if="fishData &&
                fishData.fish_species_data &&
                fishData.fish_species_data.length > 0">
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

      <v-card-actions>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" small  depressed light class="ml-2" @click="toggleLayerVisibility">
              <v-icon small>
                layers
              </v-icon>
              {{ isFishLayerVisible ? 'Hide' : 'Show'}} points on map
            </v-btn>
          </template>
          <span>{{ isFishLayerVisible ? 'Hide' : 'Show'}} Known BC Fish Observations & Distributions Layer</span>
        </v-tooltip>
      </v-card-actions>

    </v-card-text>
    <v-card-text v-else-if="!fishLoading">
      <p class="text--disabled mt-2">Unknown fish presence</p>
    </v-card-text>

    <!--FIDQ-->
    <v-card-title
      class="title mt-5 ml-3 mr-3 pa-1 mb-2"
      dark>
      Fish Inventory Data Queries
    </v-card-title>
    <v-card-text v-if="fidqLoading">
      <v-progress-linear show indeterminate></v-progress-linear>
    </v-card-text>
    <v-card-text v-if="watershed50kCodes && watershed50kCodes.length">
      <v-card-subtitle class="pr-0 pl-2">
        Search the Fish Inventory Data Queries database using the following watershed codes
      </v-card-subtitle>
      <ul>
        <template v-for="(code, i) in watershed50kCodes">
          <li :key="`fidqLink${i}`">
            <a target="_blank" :href="`http://a100.gov.bc.ca/pub/fidq/viewSingleWaterbody.do?searchCriteria.watershedCode=${code}`"
               rel="noopener">
              {{code}}
            </a>
          </li>
        </template>
      </ul>
    </v-card-text>
    <v-card-text v-else-if="!fidqLoading">
      <p class="text--disabled mt-2">
        WALLY's FIDQ search links are based on 1:20k watershed codes. No 1:20k watershed codes found in this area.
        If you believe this to be an error, please contact the Wally team to report a bug.
      </p>
    </v-card-text>
  </v-card>
  <div v-else>
    <div class="titleSub my-5">Watershed Fish Observations</div>
    <div v-if="fishLoading">
      <v-progress-linear show indeterminate></v-progress-linear>
    </div>
    <div v-if="fishData">
      <v-card flat>
        <div>
            Source:
            <a href="https://catalogue.data.gov.bc.ca/dataset/known-bc-fish-observations-and-bc-fish-distributions"
                target="_blank" rel="noopener external">
              Known BC Fish Observations and BC Fish Distributions (DataBC)
            </a>
        </div>
        <div class="my-5" v-if="fishData &&
          fishData.fish_species_data &&
          fishData.fish_species_data.length > 0">
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
        <p v-else class="text--disabled mt-2">Unknown fish presence</p>
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
  props: ['watershedID', 'surface_water_design_v2'],
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
    isFishLayerVisible: true,
    watershed50kCodes: [],
    fidqLoading: false
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
    addFishObservationsLayer (id = 'fishObservations', data, color = '#B22222', opacity = 0) {
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
      if (this.isFishLayerVisible) {
        this.$store.dispatch('map/removeMapLayer', 'fish_observations')
      } else {
        this.$store.dispatch('map/addMapLayer', 'fish_observations')
      }
      this.isFishLayerVisible = !this.isFishLayerVisible
    },
    fetchFishInventorySearchCodes () {
      this.fidqLoading = true
      ApiService.query(`/api/v1/watersheds/${this.watershedID}/fwa_50k_codes`).then((r) => {
        this.watershed50kCodes = r.data
        this.fidqLoading = false
      }).catch(e => {
        this.fidqLoading = false
        console.error(e)
      })
    }
  },
  mounted () {
    this.fetchFishObservations()
    this.fetchFishInventorySearchCodes()
  },
  beforeDestroy () {
    this.map.removeLayer('fishObservations')
    this.map.removeSource('fishObservations')
  }
}
</script>

<style>
</style>
