import ApiService, { reportingServiceURL } from '../services/ApiService'

export default {
  state: {

  },
  actions: {
    downloadFeatureReport ({ commit }, payload) {
      ApiService.post(reportingServiceURL + '/featureReport', payload, { responseType: 'arraybuffer' })
        .then((res) => {
          console.log(res)
          let blob = new Blob([res.data], { type: 'application/pdf' })
          let link = document.createElement('a')
          link.href = window.URL.createObjectURL(blob)
          link.download = 'WaterReport.pdf'
          link.click()
        }).catch((error) => {
          console.log(error)
        })
    },
    downloadLayersReport ({ commit }, payload) {
      // TODO Implement in reporting service
      // ApiService.post('http://localhost:3000' + '/layersreport', payload, {responseType: 'arraybuffer'})
      //   .then((res) => {
      //     console.log(res)
      //     let blob = new Blob([res.data], { type: 'application/pdf' })
      //     let link = document.createElement('a')
      //     link.href = window.URL.createObjectURL(blob)
      //     link.download = 'test.pdf'
      //     link.click()
      //   }).catch((error) => {
      //   console.log(error)
      // })
    }
  },
  mutations: {

  },
  getters: {

  }
}
