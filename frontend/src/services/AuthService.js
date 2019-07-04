import Keycloak from 'keycloak-js'
import EventBus from './EventBus.js'
import router from '../router.js'

const kcConfig = {
  realm: 'gwells',
  url: 'https://sso-test.pathfinder.gov.bc.ca/auth',
  publicClient: true,
  confidentialPort: 0,
  clientId: 'wally-test'
}

export class AuthService {
  kc
  accessToken
  idToken
  expiresAt
  name
  authenticated

  constructor () {
    this.kc = Keycloak(kcConfig)
  }

  init (options) {
    return new Promise((resolve, reject) => {
      this.kc.init(options).success((r) => {
        resolve()
      }).error((e) => {
        reject(new Error('unable to initialize Keycloak'))
      })
    })
  }

  setSession (next) {
    this.name = this.kc.idTokenParsed['given_name']

    // required for allowing header to update the name.
    EventBus.$emit('auth:update', { name: this.name, authenticated: this.isAuthenticated() })
    router.push(next)
  }

  login (next) {
    if (this.kc.authenticated) {
      this.setSession(next)
      return
    }
    this.kc.login().success((authenticated) => {
      this.setSession(next)
    })
  }

  logout () {
    localStorage.removeItem('loggedIn')
    localStorage.removeItem('expiresAt')
    this.kc.logout()
  }

  renewSession (ifExpiresIn = 3600) {
    return new Promise((resolve, reject) => {
      this.kc.updateToken(ifExpiresIn).success((r) => {
        if (r) {
          // successfully refreshed
        } else {
          // unsuccessful
        }
      })
    })
  }

  isAuthenticated () {
    return this.kc.authenticated
  }

  hasRole (role) {
    return this.kc.hasRealmRole(role)
  }
}
