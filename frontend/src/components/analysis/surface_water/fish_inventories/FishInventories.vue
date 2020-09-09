<template>
  <v-card flat>
    <v-card-title
      class="title mt-5 ml-3 mr-3 pa-1 mb-2"
      dark>
      Fish Inventory Data Queries
    </v-card-title>
    <v-card-text v-if="loading">
      <v-progress-linear show indeterminate></v-progress-linear>
    </v-card-text>
    <v-card-text v-if="watershed50kCodes && watershed50kCodes.length">
      <v-card-subtitle class="pr-0 pl-2">
        Search the Fish Inventory Data Queries database using the following watershed codes
      </v-card-subtitle>
      <v-btn v-on="on" small  depressed light class="ml-2"
             :href="`http://a100.gov.bc.ca/pub/fidq/viewSingleWaterbody.do?searchCriteria.watershedCode=${code}`">

        <v-icon small>
          mdi-link-variant
        </v-icon>
        Query: {{code}}
      </v-btn>
    </v-card-text>
    <v-card-text v-else-if="!loading">
      <p class="text--disabled mt-2">
        WALLY's FIDQ search links are based on 1:20k watershed codes. No 1:20k watershed codes found in this area.
        If you believe this to be an error, please contact the Wally team to report a bug.
      </p>
    </v-card-text>
  </v-card>
<!--  <v-card flat class="my-5 py-5">-->
<!--    <p class="title font-weight-bold">Fish Inventory Data Queries</p>-->
<!--    <div v-if="loading"></div>-->
<!--    <div v-else-if="watershed50kCodes && watershed50kCodes.length">-->
<!--      <p>Search the Fish Inventory Data Queries database using the following watershed codes:</p>-->
<!--      <ul>-->
<!--        <template v-for="(code, i) in watershed50kCodes">-->
<!--          <li :key="`fidqLink${i}`">-->
<!--            <a target="_blank" :href="`http://a100.gov.bc.ca/pub/fidq/viewSingleWaterbody.do?searchCriteria.watershedCode=${code}`">-->
<!--              {{code}}-->
<!--            </a>-->
<!--          </li>-->
<!--        </template>-->
<!--      </ul>-->
<!--    </div>-->
<!--    <p v-else class="text&#45;&#45;disabled">-->
<!--      WALLY's FIDQ search links are based on 1:20k watershed codes. No 1:20k watershed codes found in this area.-->
<!--      If you believe this to be an error, please contact the Wally team to report a bug.</p>-->
<!--  </v-card>-->
</template>
<script>
import ApiService from '../../../../services/ApiService'

export default {
  name: 'FishInventories',
  components: {
  },
  props: ['watershedID'],
  data: () => ({
    watershed50kCodes: [],
    loading: false
  }),
  methods: {
    fetchFishInventorySearchCodes () {
      this.loading = true
      ApiService.query(`/api/v1/watersheds/${this.watershedID}/fwa_50k_codes`).then((r) => {
        this.watershed50kCodes = r.data
        this.loading = false
      }).catch(e => {
        this.loading = false
        console.error(e)
      })
    }
  },
  mounted () {
    this.fetchFishInventorySearchCodes()
  }
}
</script>
