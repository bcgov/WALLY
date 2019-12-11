<template>
  <v-container>
    <v-row>
      <v-col cols="12" offset-md="1" md="4" align-self="center" v-if="!isFreshwaterAtlasStreamNetworksLayerEnabled">
        <div class="caption"><a href="#" @click.prevent="enableFreshwaterAtlasStreamNetworksLayer">Enable streams map layer</a></div>
      </v-col>
      <v-col>
        <span class="text-sm-right">
          <v-btn x-small v-on:click="removeOverlaps">Remove overlaps</v-btn>
        </span>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-card v-for="(stream, index) in streams" tile v-bind:key="index" v-on:click="highlight(stream)">
          <v-card-text>
            {{stream.gnis_name ? stream.gnis_name : '-'}}
            ({{stream.length_metre.toFixed(2)}}m)
            Distance: {{stream.distance.toFixed(2)}}m
            Apportionment: {{stream.apportionment.toFixed(2)}}%
            <v-icon small class="float-right" v-on:click="deleteStream(index)">mdi-trash-can</v-icon>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import qs from 'querystring'
import ApiService from '../../services/ApiService'

export default {
  name: 'StreamApportionment',
  props: ['record'],
  data: () => ({
    loading: false,
    streams: [],
    weightingFactor: 2
  }),
  methods: {
    enableFreshwaterAtlasStreamNetworksLayer () {
      this.$store.commit('addMapLayer', 'freshwater_atlas_stream_networks')
    },
    fetchStreams () {
      this.loading = true

      const params = {
        point: JSON.stringify(this.coordinates),
        get_all: true
      }
      ApiService.query(`/api/v1/streams/nearby?${qs.stringify(params)}`).then((r) => {
        this.streams = r.data.streams

        let streamData = {
          display_data_name: 'freshwater_atlas_stream_networks',
          feature_collection: {
            type: 'FeatureCollection',
            features: []
          }
        }

        this.streams.forEach((stream) => {
          streamData.feature_collection.features.push(stream.geojson)
        })

        this.$store.commit('updateHighlightFeaturesData', streamData)
      }).catch((e) => {
        console.error(e)
      }).finally(() => {
        this.loading = false
      })
    },
    highlight (stream) {
      let featureData = stream.geojson
      featureData['display_data_name'] = 'freshwater_atlas_stream_networks'
      featureData.properties['FWA_WATERSHED_CODE'] = featureData.properties['fwa_watershed_code']
      this.$store.commit('updateHighlightFeatureData', featureData)
    },
    calculateApportionment () {
      const getInverseDistance = (distance) => {
        return 1 / Math.pow(distance, this.weightingFactor)
      }

      let total = 0
      this.streams.forEach(stream => {
        stream['inverse_distance'] = getInverseDistance(stream['distance'])
        total += stream['inverse_distance']
      })

      this.streams.forEach(stream => {
        stream['apportionment'] = (stream['inverse_distance'] / total) * 100
      })
    },
    deleteStream (index) {
      if (index > -1) {
        this.streams.splice(index, 1)
        this.calculateApportionment()
      }
    },
    testFunc(){

    },
    removeOverlaps () {
      // This removes overlapping streams. It keeps the first stream in the array
      let watershedCodes = []
      let newStreamArr = []
      this.streams.forEach(stream => {
        if (!watershedCodes.includes(stream['fwa_watershed_code'])) {
          newStreamArr.push(stream)
          watershedCodes.push(stream['fwa_watershed_code'])
        }
      })
      this.streams = [...newStreamArr]
      this.calculateApportionment()
    }
  },
  computed: {
    coordinates () {
      return this.record && this.record.geometry && this.record.geometry.coordinates
    },
    isFreshwaterAtlasStreamNetworksLayerEnabled () {
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
