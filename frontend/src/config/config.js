const config = require('./config.json')

const PROD = 'production'
const STAGING = 'staging'
const DEV = 'development'

const WALLY_HOSTNAME = 'wally.pathfinder.gov.bc.ca'
const WALLY_TEST_HOSTNAME = 'wally-staging.pathfinder.gov.bc.ca'

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

global.config = envConfig
