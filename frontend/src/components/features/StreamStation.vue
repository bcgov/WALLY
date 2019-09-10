<template>
  <v-card>
    <v-card-title class="subheading font-weight-bold">
      {{ record.properties.name }}
      <span class="grey--text text--darken-2 subtitle-1">Stream monitoring station</span>
      </v-card-title>

    <v-divider></v-divider>
    <v-card-text v-if="station">
      <v-list dense>
        <v-list-item>
          <v-list-item-content>Flow data:</v-list-item-content>
          <v-list-item-content class="align-end">{{ formatYears(station.flow_years) }}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Water levels:</v-list-item-content>
          <v-list-item-content class="align-end">{{ formatYears(station.level_years) }}</v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
import ApiService from '../../services/ApiService'
export default {
  name: 'StreamStationCard',
  props: {
    record: Object
  },
  data () {
    return {
      loading: false,
      station: {}
    }
  },
  computed: {
    id () {
      return this.record.display_data_name
    }
  },
  methods: {
    fetchRecord () {
      this.loading = true
      this.station = null

      ApiService.getRaw(this.record.properties.url).then((r) => {
        this.station = r.data
      }).catch((e) => {
        this.error = e
        console.error(e)
      }).finally(() => {
        this.loading = false
      })
    },
    formatYears (val) {
      const years = val || []
      if (!years.length) {
        return 'Not available'
      }
      const min = Math.min.apply(Math, years)
      const max = Math.max.apply(Math, years)
      return `${years.length} year${years.length === 1 ? '' : 's'} between ${min} and ${max}`
    }
  },
  watch: {
    id () {
      this.fetchRecord()
    }
  },
  mounted () {
    this.fetchRecord()
  }
}
</script>

<style>

</style>
