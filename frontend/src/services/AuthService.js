import Keycloak from 'keycloak-js'

export const kcInitOptions = {
  onLoad: 'login-required',
  checkLoginIfram: false,
  pkceMethod: 'S256'
}

export const getKeycloakInstance = () => {
  return new Keycloak({
    url: process.env.VUE_APP_KC_AUTH_URL,
    realm: process.env.VUE_APP_KC_REALM,
    clientId: process.env.VUE_APP_KC_CLIENT
  })
}
