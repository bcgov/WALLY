import ApiService from '../services/ApiService'
import qs from 'querystring'
import { downloadXlsx } from '../common/utils/exportUtils'

export default {
  state: {

  },
  actions: {
    downloadExcelReport ({ commit }, payload) {
      return new Promise((resolve, reject) => {
        // Custom metrics - Track Excel downloads
        window._paq && window._paq.push([
          'trackLink',
          `${global.config.baseUrl}/api/v1/aggregate/?${qs.stringify(payload)}`,
          'download'])

        ApiService.getApi('/aggregate/?' + qs.stringify(payload), { responseType: 'arraybuffer' })
          .then((res) => {
            global.config.debug && console.log('[wally]', res)
            downloadXlsx(res, 'WaterReport.xlsx')
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
