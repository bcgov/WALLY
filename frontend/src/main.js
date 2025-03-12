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
import { getKeycloakInstance, kcInitOptions } from './services/AuthService.js'
import { mapActions } from 'vuex'
import ApiService from './services/ApiService'
import VueMatomo from 'vue-matomo'
import EventBus from './services/EventBus'
import axios from 'axios'

import './filters'

// Turn off the annoying vue production tip
Vue.config.productionTip = false

const keycloak = getKeycloakInstance()
Vue.prototype.$auth = keycloak

if (global.config.isProduction) {
  Sentry.init({
    dsn: 'https://d636fc688f55441f877594a1bf2bac89@sentry.io/1835746',
    integrations: [new Integrations.Vue({
      Vue,
      attachProps: true,
      logErrors: true
    })]
  })
  Vue.use(VueMatomo, {
    host: 'https://matomo-d1b5d2-prod.apps.silver.devops.gov.bc.ca/',
    siteId: 1,
    router,
    domains: 'wally.nrs.gov.bc.ca'
  })
}

if (global.config.isStaging) {
  Vue.use(VueMatomo, {
    host: 'https://matomo-d1b5d2-test.apps.silver.devops.gov.bc.ca/',
    siteId: 1,
    router,
    domains: '*.silver.devops.gov.bc.ca'
  })
}

if (global.config.isDevelopment && global.config.enableAnalytics) {
  // To test matomo actions locally, turn on enableAnalytics
  Vue.use(VueMatomo, {
    host: 'https://matomo-d1b5d2-test.apps.silver.devops.gov.bc.ca/',
    siteId: 1,
    router,
    domains: '*.silver.devops.gov.bc.ca',
    debug: true
  })
}

keycloak
  .init(kcInitOptions)
  .then(isAuthenticated => {
    axios.defaults.headers.common.Authorization = 'Bearer ' + keycloak.token
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
    EventBus.$emit('auth:update', { name: keycloak.idTokenParsed.display_name, authenticated: keycloak.authenticated })
  })
  .catch(err => {
    console.log(err)
  })
keycloak.onTokenExpired = function () {
  keycloak.updateToken(5)
    .then(function (refreshed) {
      if (refreshed) {
        console.log('Token was successfully refreshed')
        axios.defaults.headers.common.Authorization = 'Bearer ' + keycloak.token
      } else {
        console.log('Token is still valid')
      }
    })
    .catch(function () {
      console.warn('Failed to refresh the token, or the session has expired')
    })
}

// Test Comment
