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
        >
          <template v-slot:item.distance="{ item }">
            <span>{{item.distance.toFixed(1)}}</span>
          </template>
        </v-data-table>
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
      { text: 'Well tag number', value: 'well_tag_number', align: 'right' },
      { text: 'Distance (m)', value: 'distance', align: 'right' },
      { text: 'Static water level', value: 'static_water_level', align: 'right' },
      { text: 'Well yield', value: 'well_yield', align: 'right' }
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
        this.results = r.data
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
