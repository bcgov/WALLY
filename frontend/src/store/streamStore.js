import * as config from '../utils/streamHighlightsConfig'
import buffer from '@turf/buffer'

export default {
  state: {
    featureCollection: {
      "type": "FeatureCollection",
      "features": []
    },
    streamSources: config.sources,
    streamLayers: config.layers,
    upStreamData: {},
    downStreamData: {},
    selectedStreamData: {},
    upStreamBufferData: {},
    downStreamBufferData: {},
    selectedStreamBufferData: {}
  },
  actions: {
    calculateStreamHighlights({commit, dispatch}, payload) {
      // Get slected watershed code and trim un-needed depth
      const watershedCode = payload.stream.properties["FWA_WATERSHED_CODE"].replace(/-000000/g,'')

      // Build our downstream code list
      const codes = watershedCode.split("-")
      var downstreamCodes = [codes[0]]
      for (let i = 0; i < codes.length - 1; i++) {
        downstreamCodes.push(downstreamCodes[i] + "-" + codes[i+1])
      }

      // loop streams to find matching cases for selected, upstream, and downstream conditions
      let selectedFeatures = []
      let upstreamFeatures = []
      let downstreamFeatures = []
      payload.streams.forEach(stream => {
        const code = stream.properties["FWA_WATERSHED_CODE"].replace(/-000000/g,'') // remove empty stream ids
        if(code === watershedCode)  { selectedFeatures.push(stream) } // selected stream condition
        if(code.includes(watershedCode) && code.length > watershedCode.length)  { upstreamFeatures.push(stream) } // up stream condition
        if(downstreamCodes.indexOf(code) > -1 && code.length < watershedCode.length)  { downstreamFeatures.push(stream) } // down stream condition
      })

      // Clean out downstream features that are upwards water flow
      // TODO may want to toggle this based on user feedback
      dispatch('cleanDownStreams', { streams: downstreamFeatures, code: payload.stream.properties["FWA_WATERSHED_CODE"] })

      commit('setUpStreamData', upstreamFeatures)
      commit('setSelectedStreamData', selectedFeatures)
      // commit('setDownStreamData', cleanedDownstreamFeatures)
    },
    cleanDownStreams({ commit, dispatch }, payload) {
      let builder = payload.builder
      if(!builder) {
        builder = []
      }
      // This is a recursive function that walks down the stream network
      // from the selected stream segment location. It removes any stream
      // segments that are at the same order but have an upwards stream flow.
      // Returns an array (builder) of cleaned stream segment features.
      // The BigO of this function is linear with a max of apprx. 50 due
      // to the max magnitude of a stream
      var segment = payload.streams.find((s) => {
        if(s.properties["LOCAL_WATERSHED_CODE"]) {
          let local = s.properties["LOCAL_WATERSHED_CODE"]
          let global = s.properties["FWA_WATERSHED_CODE"]
          if(local === payload.code && global !== local) {
            return s
          }
        }
      })
      if(segment) {
        let drm = segment.properties["DOWNSTREAM_ROUTE_MEASURE"]
        let segmentCode = segment.properties["FWA_WATERSHED_CODE"]
        let elements = payload.streams.filter((f) => { 
          if(f.properties["FWA_WATERSHED_CODE"] === segmentCode && 
            f.properties["DOWNSTREAM_ROUTE_MEASURE"] < drm){
              return f
            }
        })
        builder = builder.concat(elements)
        // Recursive call step with current builder object and next segment selection
        return dispatch('cleanDownStreams', { streams: payload.streams, code: segmentCode, builder: builder })
      } else {
        commit('setDownStreamData', builder)
      }
    }
  },
  mutations: {
    setUpStreamData (state, payload) {
      let collection = Object.assign({}, state.featureCollection) 
      collection["features"] = payload
      state.upStreamData = collection
    },
    setDownStreamData (state, payload) {
      let collection = Object.assign({}, state.featureCollection) 
      collection["features"] = payload
      state.downStreamData = collection
    },
    setSelectedStreamData (state, payload) {
      let collection = Object.assign({}, state.featureCollection) 
      collection["features"] = payload
      state.selectedStreamData = collection
    },
    resetStreamData (state) {
      state.upStreamData = state.featureCollection
      state.downStreamData = state.featureCollection
      state.selectedStreamData = state.featureCollection
    },
    setStreamBufferData (state, payload) {
      state.upStreamBufferData = buffer(state.upStreamData, payload)
      state.downStreamBufferData = buffer(state.downStreamData, payload)
      state.selectedStreamBufferData = buffer(state.selectedStreamData, payload)
    },
    resetStreamBufferData (state) {
      state.upStreamBufferData = state.featureCollection
      state.downStreamBufferData = state.featureCollection
      state.selectedStreamBufferData = state.featureCollection
    }
  },
  getters: {
    getUpStreamData: state => state.upStreamData,
    getDownStreamData: state => state.downStreamData,
    getSelectedStreamData: state => state.selectedStreamData,
    getStreamSources: state => state.streamSources,
    getStreamLayers: state => state.streamLayers,
    getUpStreamBufferData: state => state.upStreamBufferData,
    getDownStreamBufferData: state => state.downStreamBufferData,
    getSelectedStreamBufferData: state => state.selectedStreamBufferData
  }
}
