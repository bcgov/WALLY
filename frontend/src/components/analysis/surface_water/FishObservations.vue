<template>
  <div>
    <div class="titleSub my-5">Watershed Fish Observations</div>
    <div v-if="fishLoading">
      <v-progress-linear show indeterminate></v-progress-linear>
    </div>
    <div v-if="fishData">
      <v-card flat>
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
        </div>
      </v-card>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import ApiService from '../../../services/ApiService'

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
      { text: 'Observation Count', value: 'count', align: 'center'},
      { text: 'Life Stages Observed', value: 'life_stages', align: 'center'},
      { text: 'First Observation Date', value: 'observation_date_min', align: 'center'},
      { text: 'Last Observation Date', value: 'observation_date_max', align: 'center'},
    ]
  }),
  computed: {
    ...mapGetters('map', ['map'])
  },
  watch: {
    watershedID () {
    //   this.map.removeLayer('fishObservations')
    //   this.map.removeSource('fishObservations')
      this.fetchFishObservations()
    }
  },
  methods: {
    fetchFishObservations () {
      this.fishData = null
      this.fishLoading = true
      ApiService.query(`/api/v1/watersheds/${this.watershedID}/fish_observations`)
        .then(r => {
          this.fishData = r.data

        //   const max = Math.max(...r.data.licences.features.map(x => Number(x.properties.qty_m3_yr)))
        //   this.addLicencesLayer('waterLicences', r.data.licences, '#00796b', 0.5, max)
        //   this.setPurposeTypes()

          this.fishLoading = false
        })
        .catch(e => {
          this.fishLoading = false
          console.error(e)
        })
    }
  },
  mounted () {
    this.fetchFishObservations()
  },
  beforeDestroy () {
    // this.map.removeLayer('fishObservations')
    // this.map.removeSource('fishObservations')
  }
}
</script>

<style>
</style>
