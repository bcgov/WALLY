import Vue from 'vue'
import vuetify from './plugins/vuetify'
// import * as Sentry from '@sentry/browser'
// import * as Integrations from '@sentry/integrations'
import './config/config'
import App from './App'
import router from './router'
import store from './store'
import * as Sentry from '@sentry/browser'
import * as Integrations from '@sentry/integrations'
import { AuthService } from './services/AuthService.js'
import { mapActions } from 'vuex'
import ApiService from './services/ApiService'
import VueMatomo from 'vue-matomo'

import './filters'

// Turn off the annoying vue production tip
Vue.config.productionTip = false

const auth = new AuthService()
Vue.prototype.$auth = auth

if (global.config.isProduction) {
  Sentry.init({
    dsn: 'https://d636fc688f55441f877594a1bf2bac89@sentry.io/1835746',
    integrations: [new Integrations.Vue({ Vue,
      attachProps: true,
      logErrors: true })]
  })
  Vue.use(VueMatomo, {
    host: 'https://matomo-d1b5d2-prod.apps.silver.devops.gov.bc.ca/',
    siteId: 1,
    router: router,
    domains: '*.nrs.gov.bc.ca'
  })
}

if (global.config.isStaging) {
  Vue.use(VueMatomo, {
    host: 'https://matomo-d1b5d2-test.apps.silver.devops.gov.bc.ca/',
    siteId: 1,
    router: router,
    domains: '*.silver.devops.gov.bc.ca'
  })
}

if (global.config.isDevelopment && global.config.enableAnalytics) {
  // To test matomo actions locally, turn on enableAnalytics
  Vue.use(VueMatomo, {
    host: 'https://matomo-d1b5d2-test.apps.silver.devops.gov.bc.ca/',
    siteId: 1,
    router: router,
    domains: '*.silver.devops.gov.bc.ca',
    debug: true
  })
}

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
