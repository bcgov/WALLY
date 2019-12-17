import { mapGetters } from 'vuex'
import qs from 'querystring'
import ApiService from '../../services/ApiService'

export default {
  name: 'StreamApportionment',
  props: ['record'],
  data: () => ({
    loading: false,
    streams: [],
    selected: [],
    weightingFactor: 2,
    apportionmentMin: 10,
    multiSelect: false,
    show: {
      reloadAll: false,
      removeOverlaps: true,
      removeLowApportionment: true
    },
    weightingFactorValidation: {
      required: value => !!value || 'Required',
      number: value => !Number.isNaN(parseFloat(value)) || 'Invalid number',
      max: value => (value >= 2 && value <= 3) || 'Weighting factor must be' +
        ' either 2 or 3'
    },
    headers: [
      { text: 'GNIS Name', value: 'gnis_name' },
      { text: 'Length (m)', value: 'length_metre', align: 'end' },
      { text: 'Distance (m)', value: 'distance', align: 'end' },
      { text: 'Apportionment', value: 'apportionment', align: 'end' },
      { text: '', value: 'action', sortable: false }
    ]
  }),
  methods: {
    enableFreshwaterAtlasStreamNetworksLayer () {
      this.$store.commit('addMapLayer', 'freshwater_atlas_stream_networks')
    },
    toggleMultiSelect () {
      this.multiSelect = !this.multiSelect
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

        this.show.reloadAll = false
        this.show.removeOverlaps = true
        this.show.removeLowApportionment = true

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
      this.loading = true
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
      this.loading = false
    },
    deleteStream (selectedStream) {
      let newStreamArr = this.streams.filter(stream => {
        return stream['ogc_fid'] !== selectedStream['ogc_fid']
      })
      this.streams = [...newStreamArr]
      this.show.reloadAll = true
      this.calculateApportionment()
    },
    removeSelected () {
      // Remove user-selected streams and recalculate apportionment
      let selectedIds = this.selected.map(selected => selected['ogc_fid'])
      let newStreamArr = this.streams.filter(stream => {
        return !selectedIds.includes(stream['ogc_fid'])
      })
      this.streams = [...newStreamArr]
      this.show.reloadAll = true
      this.calculateApportionment()
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
      this.show.removeOverlaps = false
      this.show.reloadAll = true
      this.calculateApportionment()
    },
    removeStreamsWithLowApportionment (apportionment) {
      // Keep streams that have more than x% apportionment
      let newStreamArr = this.streams.filter(stream => {
        return stream['apportionment'] > apportionment
      })
      this.streams = [...newStreamArr]
      this.show.removeLowApportionment = false
      this.show.reloadAll = true
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
    },
    weightingFactor (value) {
      if (value > 1 && value < 4) {
        this.calculateApportionment()
      }
    }
  },
  mounted () {
    this.fetchStreams()
  },
  beforeDestroy () {
  }
}
