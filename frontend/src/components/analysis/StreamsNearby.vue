<template>
  <v-container>
    <v-row>
      <v-col>
        Test
      </v-col>
      <v-col cols="12" offset-md="1" md="4" align-self="center" v-if="!isFreshwaterAtlasStreamNetworksLayerEnabled">
        <div class="caption"><a href="#" @click.prevent="enableFreshwaterAtlasStreamNetworksLayer">Enable streams map layer</a></div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import qs from 'querystring'
import ApiService from '../../services/ApiService'
import debounce from 'lodash.debounce'

export default {
  name: 'StreamsNearby',
  props: ['record'],
  data: () => ({
    loading: false,
    streams: []
  }),
  methods: {
    enableFreshwaterAtlasStreamNetworksLayer() {
      this.$store.commit('addMapLayer', 'freshwater_atlas_stream_networks')
    },
    fetchStreams () {
      this.loading = true

      const params = {
        point: JSON.stringify(this.coordinates)
      }
      ApiService.query(`/api/v1/streams/nearby?${qs.stringify(params)}`).then((r) => {
        this.streams = r.data.streams
      }).catch((e) => {
        console.error(e)
      }).finally(() => {
        this.loading = false
      })
    }
  },
  computed: {
    coordinates () {
      return this.record && this.record.geometry && this.record.geometry.coordinates
    },
    isFreshwaterAtlasStreamNetworksLayerEnabled() {
      return this.isMapLayerActive('freshwater_atlas_stream_networks')
    },
    ...mapGetters(['isMapLayerActive'])
  },
  watch: {
    record: {
      handler () {
        this.fetchStreams()
      },
      deep: true
    },
    coordinates () {
      this.fetchStreams()
    }
  },
  mounted () {
    this.fetchStreams()
  },
  beforeDestroy () {
  }
}
</script>

<style>

</style>
