<template>
  <div>
    <v-row>
      <v-col>

      </v-col>
    </v-row>
  </div>
</template>

<script>
import qs from 'querystring'
import ApiService from '../../services/ApiService'
import EventBus from '../../services/EventBus'

export default {
  name: 'WellsCrossSection',
  props: ['record', 'coordinates'],
  data: () => ({
    radius: 200,
    results: [],
    loading: false
  }),
  methods: {
    fetchWellsAlongLine () {
      const params = {
        radius: parseFloat(this.radius),
        line: JSON.stringify(this.coordinates)
      }
      ApiService.query(`/api/v1/analysis/wells/section?${qs.stringify(params)}`).then((r) => {
        this.results = r.data.wells
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
  }
}
</script>

<style>

</style>
