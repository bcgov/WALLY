<template>
  <div>
    <v-row>
      <v-col cols="12" md="4">
        <v-text-field
          label="Search radius (m)"
          placeholder="1000"
          v-model="radius"
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-data-table
          :loading="loading"
          :headers="headers"
          :items="results"
        ></v-data-table>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import qs from 'querystring'
import ApiService from '../../services/ApiService'
export default {
  name: 'DistanceToWells',
  props: ['record', 'coordinates'],
  data: () => ({
    radius: 1000,
    results: [],
    loading: false,
    headers: [
      { text: 'Well tag number', value: 'well_tag_number' },
      { text: 'Distance (m)', value: 'distance' }
    ]
  }),
  methods: {
    fetchWells () {
      this.loading = true
      const params = {
        radius: this.radius,
        point: JSON.stringify(this.coordinates)
      }
      ApiService.query(`/api/v1/analysis/wells/nearby?${qs.stringify(params)}`).then((r) => {
        this.results = r.data.map((x) => ({
          well_tag_number: Number(x[0]),
          distance: x[1].toFixed(1)
        }))
        console.log(this.results)
      }).catch((e) => {
        console.error(e)
      }).finally(() => {
        this.loading = false
      })
    }
  },
  watch: {
    record: {
      handler () {
        this.fetchWells()
      },
      deep: true
    },
    coordinates () {
      this.fetchWells()
    }
  },
  mounted () {
    this.fetchWells()
  }
}
</script>

<style>

</style>
