import Vue from 'vue'
import Vuetify from 'vuetify'
import './plugins/vuetify'
import App from './App'
import router from './router'
import store from './store'

import { AuthService } from './services/AuthService.js'

Vue.config.productionTip = false
Vue.use(Vuetify)

const auth = new AuthService()
Vue.prototype.$auth = auth

auth.init({
  onLoad: 'check-sso',
  checkLoginIframe: true,
  timeSkew: 10
}).then(() => {
  new Vue({
    router,
    store,
    render: h => h(App)
  }).$mount('#app')
})
