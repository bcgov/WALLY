import ApiService, { reportingServiceURL } from '../services/ApiService'
import qs from 'querystring'

export default {
  state: {

  },
  actions: {
    downloadPDFReport ({ commit }, payload) {
      // note: the null here is for the "record" option of the ApiService.get method.
      return new Promise((resolve, reject) => {
        ApiService.get(reportingServiceURL + '/featureReport?' + qs.stringify(payload), null, { responseType: 'arraybuffer' })
          .then((res) => {
            console.log(res)
            let blob = new Blob([res.data], { type: 'application/pdf' })
            let link = document.createElement('a')
            link.href = window.URL.createObjectURL(blob)
            link.download = 'WaterReport.pdf'
            document.body.appendChild(link)
            link.click()
            setTimeout(() => {
              document.body.removeChild(link)
              window.URL.revokeObjectURL(link.href)
            }, 0)
            resolve(true)
          }).catch((error) => {
            reject(error)
          })
      })
    },
    downloadExcelReport ({ commit }, payload) {
      return new Promise((resolve, reject) => {
        ApiService.getApi('/aggregate?' + qs.stringify(payload), { responseType: 'arraybuffer' })
          .then((res) => {
            console.log(res)
            let blob = new Blob([res.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
            let link = document.createElement('a')
            link.href = window.URL.createObjectURL(blob)
            link.download = 'WaterReport.xlsx'
            document.body.appendChild(link)
            link.click()
            setTimeout(() => {
              document.body.removeChild(link)
              window.URL.revokeObjectURL(link.href)
            }, 0)
            resolve(true)
          }).catch((error) => {
            reject(error)
          })
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
