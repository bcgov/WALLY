const config = require('./config.json')

const PROD = 'production'
const STAGING = 'staging'
const DEV = 'development'

const WALLY_HOSTNAME = 'wally.nrs.gov.bc.ca'
const WALLY_TEST_HOSTNAME = 'wally-staging.apps.silver.devops.gov.bc.ca'

config.app.baseUrl = window.location.protocol + '//' +
  location.host.split(':')[0] +
  ((window.location.port) && ':' + window.location.port)

// Development - envConfig is not defined yet
let envConfig = config[DEV]

// Production
if (process.env.VUE_APP_ENV === 'production' &&
  window.location.hostname === WALLY_HOSTNAME) {
  envConfig = config[PROD]
}

// Staging
if (window.location.hostname === WALLY_TEST_HOSTNAME) {
  envConfig = config[STAGING]
}

const finalConfig = { ...config['app'], ...envConfig }
global.config = finalConfig
