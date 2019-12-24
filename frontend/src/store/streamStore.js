import * as config from '../utils/streamHighlights.config'
import buffer from '@turf/buffer'
import _ from 'lodash'

export default {
  state: {
    featureCollection: {
      'type': 'FeatureCollection',
      'features': []
    },
    streamSources: config.sources,
    streamLayers: config.layers,
    upstreamData: {},
    downstreamData: {},
    selectedStreamData: {},
    upstreamBufferData: {},
    downstreamBufferData: {},
    selectedStreamBufferData: {}
  },
  actions: {
    /*
    fetchConnectedStreams ({ commit, dispatch }, payload) {
      // NOTE this action is the server backed query but at this point is too slow to implement
      let fwaCode = payload.stream.properties['FWA_WATERSHED_CODE']
      let outflowCode = fwaCode.substring(0, fwaCode.indexOf('-') + 1)

      ApiService.query(`/api/v1/analysis/stream/connections?outflowCode=${outflowCode}`)
        .then((response) => {
          console.log(response.data)
          let params = {
            stream: payload.stream,
            streams: response.data
          }
          dispatch('calculateStreamHighlights', params)
        })
        .catch((error) => {
          console.log(error)
        })
    },
    */
    calculateStreamHighlights ({ commit, dispatch }, payload) {
      // Get selected watershed code and trim un-needed depth
      const watershedCode = payload.stream.properties['FWA_WATERSHED_CODE'].replace(/-000000/g, '')

      // Build our downstream code list
      const codes = watershedCode.split('-')
      let downstreamCodes = [codes[0]]
      for (let i = 0; i < codes.length - 1; i++) {
        downstreamCodes.push(downstreamCodes[i] + '-' + codes[i + 1])
      }

      // loop streams to find matching cases for selected, upstream, and downstream conditions
      let selectedFeatures = []
      let upstreamFeatures = []
      let downstreamFeatures = []
      payload.streams.forEach(stream => {
        const code = stream.properties['FWA_WATERSHED_CODE'].replace(/-000000/g, '') // remove empty stream ids
        if (code === watershedCode) { selectedFeatures.push(stream) } // selected stream condition

        if (code.includes(watershedCode) && code.length > watershedCode.length) { upstreamFeatures.push(stream) } // up stream condition
        if (downstreamCodes.indexOf(code) > -1 && code.length < watershedCode.length) { downstreamFeatures.push(stream) } // down stream condition
      })

      // Clean out downstream features that are upwards water flow
      // TODO may want to toggle this based on user feedback
      dispatch('cleanDownstreams', { streams: downstreamFeatures, code: payload.stream.properties['FWA_WATERSHED_CODE'] })
      dispatch('cleanDownstreams', { streams: downstreamFeatures, code: payload.stream.properties['FWA_WATERSHED_CODE'] })

      commit('setUpstreamData', upstreamFeatures)
      commit('setSelectedStreamData', selectedFeatures)
      // commit('setDownstreamData', cleanedDownstreamFeatures)
    },
    cleanDownstreams ({ commit, dispatch }, payload) {
      let builder = payload.builder
      if (!builder) {
        builder = []
      }
      // This is a recursive function that walks down the stream network
      // from the selected stream segment location. It removes any stream
      // segments that are at the same order but have an upwards stream flow.
      // Returns an array (builder) of cleaned stream segment features.
      // The BigO of this function is linear with a max of apprx. 50 due
      // to the max magnitude of a stream
      let segment = payload.streams.find((s) => {
        if (s.properties['LOCAL_WATERSHED_CODE']) {
          let local = s.properties['LOCAL_WATERSHED_CODE']
          let global = s.properties['FWA_WATERSHED_CODE']
          if (local === payload.code && global !== local) {
            return s
          }
        }
      })
      if (segment) {
        let drm = segment.properties['DOWNSTREAM_ROUTE_MEASURE']
        let segmentCode = segment.properties['FWA_WATERSHED_CODE']
        let elements = payload.streams.filter((f) => {
          if (f.properties['FWA_WATERSHED_CODE'] === segmentCode &&
            f.properties['DOWNSTREAM_ROUTE_MEASURE'] < drm) {
            return f
          }
        })
        builder = builder.concat(elements)
        // Recursive call step with current builder object and next segment selection
        return dispatch('cleanDownstreams', { streams: payload.streams, code: segmentCode, builder: builder })
      } else {
        commit('setDownstreamData', builder)
      }
    }
  },
  mutations: {
    setUpstreamData (state, payload) {
      let collection = Object.assign({}, state.featureCollection)
      collection['features'] = _.unionBy(payload, state.upStreamData.features, x => x.properties.LINEAR_FEATURE_ID + x.geometry.coordinates[0])
      state.upStreamData = collection
    },
    setDownstreamData (state, payload) {
      let collection = Object.assign({}, state.featureCollection)
      collection['features'] = _.unionBy(payload, state.downstreamData.features, x => x.properties.LINEAR_FEATURE_ID + x.geometry.coordinates[0])
      state.downstreamData = collection
    },
    setSelectedStreamData (state, payload) {
      let collection = Object.assign({}, state.featureCollection)
      collection['features'] = _.unionBy(payload, state.selectedStreamData.features, x => x.properties.LINEAR_FEATURE_ID + x.geometry.coordinates[0])
      state.selectedStreamData = collection
    },
    resetStreamData (state) {
      state.upstreamData = state.featureCollection
      state.downstreamData = state.featureCollection
      state.selectedStreamData = state.featureCollection
    },
    setStreamBufferData (state, payload) {
      state.upstreamBufferData = buffer(state.upstreamData, payload, { units: 'meters' })
      state.downstreamBufferData = buffer(state.downstreamData, payload, { units: 'meters' })
      state.selectedStreamBufferData = buffer(state.selectedStreamData, payload, { units: 'meters' })
    },
    setUpstreamBufferData (state, payload) {
      state.upstreamBufferData = buffer(state.upstreamData, payload, { units: 'meters' })
    },
    setDownstreamBufferData (state, payload) {
      state.downstreamBufferData = buffer(state.downstreamData, payload, { units: 'meters' })
    },
    setSelectedStreamBufferData (state, payload) {
      state.selectedStreamBufferData = buffer(state.selectedStreamData, payload, { units: 'meters' })
    },
    resetStreamBufferData (state) {
      state.upstreamBufferData = state.featureCollection
      state.downstreamBufferData = state.featureCollection
      state.selectedStreamBufferData = state.featureCollection
    },
    setStreamAnalysisPanel (state, payload) {
      state.streamAnalysisPanelOpen = payload
    }
  },
  getters: {
    getUpstreamData: state => state.upstreamData,
    getDownstreamData: state => state.downstreamData,
    getSelectedStreamData: state => state.selectedStreamData,
    getStreamSources: state => state.streamSources,
    getStreamLayers: state => state.streamLayers,
    getUpstreamBufferData: state => state.upstreamBufferData,
    getDownstreamBufferData: state => state.downstreamBufferData,
    getSelectedStreamBufferData: state => state.selectedStreamBufferData
  }
}
