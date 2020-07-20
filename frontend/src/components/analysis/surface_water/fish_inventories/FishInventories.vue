<template>
  <v-card flat class="my-5 py-5">
    <p class="title font-weight-bold">Fish Inventory Data Queries</p>
    <div v-if="loading"></div>
    <div v-else-if="watershed50kCodes && watershed50kCodes.length">
      <p>Search the Fish Inventory Data Queries database using the following watershed codes:</p>
      <ul>
        <template v-for="(code, i) in watershed50kCodes">
          <li :key="`fidqLink${i}`">
            <a target="_blank" :href="`http://a100.gov.bc.ca/pub/fidq/viewSingleWaterbody.do?searchCriteria.watershedCode=${code}`">
              {{code}}
            </a>
          </li>
        </template>
      </ul>
    </div>
    <p v-else class="text--disabled">
      WALLY's FIDQ search links are based on 1:20k watershed codes. No 1:20k watershed codes found in this area.
      If you believe this to be an error, please contact the Wally team to report a bug.</p>
  </v-card>
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
