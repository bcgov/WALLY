import ApiService from '../services/ApiService'
import qs from 'querystring'

export default {
  state: {

  },
  actions: {
    downloadExcelReport ({ commit }, payload) {
      return new Promise((resolve, reject) => {
        // Custom metrics - Track Excel downloads
        window._paq.push([
          'trackLink',
          `${process.env.VUE_APP_AXIOS_BASE_URL}/api/v1/aggregate/?${qs.stringify(payload)}`,
          'download'])

        ApiService.getApi('/aggregate/?' + qs.stringify(payload), { responseType: 'arraybuffer' })
          .then((res) => {
            global.config.debug && console.log('[wally]', res)
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
    }
  },
  mutations: {

  },
  getters: {

  }
}
