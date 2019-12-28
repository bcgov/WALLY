import Vue from 'vue'
import vuetify from './plugins/vuetify'
import * as Sentry from '@sentry/browser'
import * as Integrations from '@sentry/integrations'
import App from './App'
import router from './router'
import store from './store'

import { AuthService } from './services/AuthService.js'
import { mapActions } from 'vuex'
import ApiService from './services/ApiService'

Vue.config.productionTip = false

const auth = new AuthService()
Vue.prototype.$auth = auth

// Sentry.init({
//   dsn: 'https://d636fc688f55441f877594a1bf2bac89@sentry.io/1835746',
//   integrations: process.env.VUE_APP_ENV === 'production' ? [new Integrations.Vue({ Vue,
//     attachProps: true,
//     logErrors: true })] : []
// })

auth.init({
  onLoad: 'check-sso',
  checkLoginIframe: true,
  timeSkew: 10
}).then(() => {
  new Vue({
    vuetify,
    router,
    store,
    methods: {
      ...mapActions([
        'getMapLayers'
      ])
    },
    created () {
      ApiService.init()
    },
    render: h => h(App)
  }).$mount('#app')
})
