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
      values: value => (
        parseFloat(value) === 1 || parseFloat(value) === 2
      ) || 'Weighting factor must be either 1 (linear) or 2 (squared)'
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
      this.$store.commit('map/addMapLayer', 'freshwater_atlas_stream_networks')
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

        this.show.reloadAll = false
        this.show.removeOverlaps = true
        this.show.removeLowApportionment = true

        this.highlightStreams()
      }).catch((e) => {
        console.error(e)
      }).finally(() => {
        this.loading = false
      })
    },
    highlight (stream) {
      let featureStream = stream.geojson
      featureStream['display_data_name'] = 'freshwater_atlas_stream_networks'
      featureStream.properties['FWA_WATERSHED_CODE'] = featureStream.properties['fwa_watershed_code']
      this.$store.commit('updateHighlightFeatureData', featureStream)

      let featureDistanceLines = {
        'type': 'Feature',
        'geometry': {
          'type': 'LineString',
          'coordinates': [
            this.coordinates,
            stream['closest_stream_point']['coordinates']
          ]
        },
        'properties': {
          'title': stream['distance'].toFixed(2) + 'm'
        }
      }

      let featureClosestPoint = {
        'type': 'Feature',
        'geometry': {
          'type': 'Point',
          'coordinates': stream['closest_stream_point']['coordinates']
        },
        'properties': {
          'title': stream['distance'].toFixed(2) + 'm'
        }
      }

      let streamData = {
        display_data_name: 'stream_apportionment',
        feature_collection: {
          type: 'FeatureCollection',
          features: [featureClosestPoint, featureDistanceLines]
        }
      }

      // Highlight the stream
      this.$store.commit('updateHighlightFeatureData', featureStream)
      // Highlight the closest point & distance line to that stream
      this.$store.commit('updateHighlightFeatureCollectionData', streamData)
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
    reloadStreams () {
      this.loading = true
      this.calculateApportionment()
      this.highlightStreams()
      this.loading = false
    },
    deleteStream (selectedStream) {
      let newStreamArr = this.streams.filter(stream => {
        return stream['ogc_fid'] !== selectedStream['ogc_fid']
      })
      this.streams = [...newStreamArr]
      this.show.reloadAll = true
      this.reloadStreams()
    },
    removeSelected () {
      // Remove user-selected streams
      let selectedIds = this.selected.map(selected => selected['ogc_fid'])
      let newStreamArr = this.streams.filter(stream => {
        return !selectedIds.includes(stream['ogc_fid'])
      })
      this.streams = [...newStreamArr]
      this.show.reloadAll = true
      this.reloadStreams()
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
      this.reloadStreams()
    },
    removeStreamsWithLowApportionment (apportionment) {
      // Keep streams that have more than x% apportionment
      let newStreamArr = this.streams.filter(stream => {
        return stream['apportionment'] > apportionment
      })
      this.streams = [...newStreamArr]
      this.show.removeLowApportionment = false
      this.show.reloadAll = true
      this.reloadStreams()
    },
    highlightStreams () {
      let streamData = {
        display_data_name: 'freshwater_atlas_stream_networks',
        feature_collection: {
          type: 'FeatureCollection',
          features: []
        }
      }
      let distanceLines = []
      let closestPoints = []

      this.streams.forEach((stream) => {
        streamData.feature_collection.features.push(stream.geojson)

        let closestPoint = {
          'type': 'Feature',
          'geometry': stream['closest_stream_point'],
          'properties': {
            'title': ''
          }
        }
        closestPoints.push(closestPoint)

        const distanceLineCoordinates = [this.coordinates,
          stream['closest_stream_point']['coordinates']
        ]

        let distanceLine = {
          'type': 'Feature',
          'geometry': {
            'type': 'LineString',
            'coordinates': distanceLineCoordinates
          },
          'properties': {
            'title': stream['distance'].toFixed(2) + 'm'
          }
        }
        distanceLines.push(distanceLine)
      })

      const highlightData = {
        display_data_name: 'stream_apportionment',
        feature_collection: {
          type: 'FeatureCollection',
          features: [
            ...closestPoints,
            ...distanceLines
          ]
        }
      }

      this.$store.commit('updateHighlightFeatureCollectionData', highlightData)
    }
  },
  computed: {
    coordinates () {
      return this.record && this.record.geometry && this.record.geometry.coordinates
    },
    isFreshwaterAtlasStreamNetworksLayerEnabled () {
      return this.isMapLayerActive('freshwater_atlas_stream_networks')
    },
    ...mapGetters('map', ['isMapLayerActive'])
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
      if (parseFloat(value) === 1 || parseFloat(value) === 2) {
        this.calculateApportionment()
      }
    }
  },
  mounted () {
    this.fetchStreams()
    if (!this.isFreshwaterAtlasStreamNetworksLayerEnabled) {
      this.enableFreshwaterAtlasStreamNetworksLayer()
    }
  },
  beforeDestroy () {
    console.log('before destroy')
    this.$store.commit('updateHighlightFeatureCollectionData', {})
  }
}
