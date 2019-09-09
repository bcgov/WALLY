import EventBus from '../services/EventBus.js'
import ApiService from '../services/ApiService.js'

export default {
  state: {
    activeDataMarts: [],
    displayTemplates: [],
    dataMartFeatureInfo: { content: { properties: {} } },
    dataMartFeatures: [] // selected points
  },
  actions: {
    getDataMart ({ commit }, payload) {
      // Get the datamart either via API or wms layer
      const { displayDataName, url } = payload
      ApiService.getRaw(url).then((response) => {
        commit('addDataMart', {
          displayDataName: displayDataName,
          data: response.data
        })
        EventBus.$emit(`dataMart:updated`, payload)
      }).catch((error) => {
        console.log(error) // TODO create error state item and mutation
      })
    },
    getDataMartFeatureInfo ({ commit }, payload) {
      // WMS request
      // TODO: Complete this request
      ApiService.getRaw(payload.url).then((res) => {
        // TODO validate properties
        commit('setDataMartFeatureInfo', {
          displayDataName: res.data.features[0].id,
          coordinates: [payload.lat, payload.lng],
          properties: res.data.features[0].properties })
        EventBus.$emit(`feature:added`, payload)
      }).catch((error) => {
        console.log(error) // TODO create error state item and mutation
      })
    },
    getDataMartFeatures ({ commit }, payload) {
      var layers = payload.layers.map((x) => {
        return 'layers=' + x.display_data_name + '&'
      })

      var bbox = payload.bounds
      bbox = bbox.map((x) => {
        return 'bbox=' + x + '&'
      })

      var width = 'width=' + payload.size.x + '&'
      var height = 'height=' + payload.size.y

      var params = layers.join('') + bbox.join('') + width + height

      // "layers=automated_snow_weather_station_locations&layers=ground_water_wells&bbox=-123.5&bbox=49&bbox=-123&bbox=50&width=500&height=500"
      ApiService.getApi('/aggregate?' + params)
        .then((response) => {
          // console.log('response for aggregate', response)
          let displayData = response.data.display_data
          let displayTemplates = response.data.display_templates

          displayData.forEach(layer => {
            commit('setDataMartFeatures', { [layer.layer]: layer.geojson.features })
          })
          commit('setDisplayTemplates', { displayTemplates })
        }).catch((error) => {
          console.log(error)
        })
    }
  },
  mutations: {
    setDataMartFeatureInfo: (state, payload) => {
      state.dataMartFeatureInfo = payload
    },
    setDataMartFeatures: (state, payload) => { state.dataMartFeatures.push(payload) },
    setDisplayTemplates: (state, payload) => { state.displayTemplates = payload },
    clearDataMartFeatures: (state) => { state.dataMartFeatures = [] },
    addDataMart (state, payload) {
      state.activeDataMarts.push(payload)
      EventBus.$emit(`dataMart:added`, payload)
    },
    removeDataMart (state, payload) {
      state.activeDataMarts = state.activeDataMarts.filter(function (source) {
        return source.displayDataName !== payload
      })
      EventBus.$emit(`dataMart:removed`, payload)
    }
  },
  getters: {
    displayTemplates: state => state.displayTemplates,
    dataMartFeatureInfo: state => state.dataMartFeatureInfo,
    dataMartFeatures: state => state.dataMartFeatures,
    activeDataMarts: state => state.activeDataMarts,
    isDataMartActive: state => displayDataName => !!state.activeDataMarts.find((x) => x && x.displayDataName === displayDataName),
    allDataMarts: () => [], // ideally grab these from the meta data api
  }
}
