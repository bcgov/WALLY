import Vue from 'vue'
import vuetify from './plugins/vuetify'
// import * as Sentry from '@sentry/browser'
// import * as Integrations from '@sentry/integrations'
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

Vue.config.productionTip = false

const WALLY_HOSTNAME = 'wally.pathfinder.gov.bc.ca'
const WALLY_TEST_HOSTNAME = 'wally-staging.pathfinder.gov.bc.ca'

const auth = new AuthService()
Vue.prototype.$auth = auth

if (process.env.VUE_APP_ENV === 'production' &&
    window.location.hostname === WALLY_HOSTNAME
) {
  Sentry.init({
    dsn: 'https://d636fc688f55441f877594a1bf2bac89@sentry.io/1835746',
    integrations: [new Integrations.Vue({ Vue,
      attachProps: true,
      logErrors: true })]
  })
  Vue.use(VueMatomo, {
    host: 'https://matomo-bfpeyx-prod.pathfinder.gov.bc.ca/',
    siteId: 1,
    router: router,
    domains: '*.pathfinder.gov.bc.ca'
  })
}

if (window.location.hostname === WALLY_TEST_HOSTNAME) {
  // To test matomo actions locally just move the below plugin code outside
  // of this if check, otherwise this will only log actions from staging
  Vue.use(VueMatomo, {
    host: 'https://matomo-bfpeyx-test.pathfinder.gov.bc.ca/',
    siteId: 1,
    router: router,
    domains: '*.pathfinder.gov.bc.ca'
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
