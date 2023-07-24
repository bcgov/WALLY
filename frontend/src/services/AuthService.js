
import Keycloak from 'keycloak-js'

export const kcInitOptions = {
  onLoad: 'login-required',
  checkLoginIfram: false,
  pkceMethod: 'S256'
}

export const getKeycloakInstance = () => {
  let keyCloakAuthUrl
  if (global.config.isProduction) {
    keyCloakAuthUrl = 'https://loginproxy.gov.bc.ca/auth'
  } else if (global.config.isStaging) {
    keyCloakAuthUrl = 'https://test.loginproxy.gov.bc.ca/auth'
  } else {
    keyCloakAuthUrl = 'https://dev.loginproxy.gov.bc.ca/auth'
  }
  return new Keycloak({
    url: keyCloakAuthUrl,
    realm: 'standard',
    clientId: 'wally-4389'
  })
}
