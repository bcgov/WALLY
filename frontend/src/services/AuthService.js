import EventBus from './EventBus.js'
import router from '../router.js'
import Axios from 'axios'

export class AuthService {
  accessToken
  idToken
  name
  authenticated

  init (options) {
    return new Promise((resolve, reject) => {
      // local environment pseudo-token.  All tokens/sessions are handled by Keycloak gatekeeper, so
      // the vue app is not responsible for any token handling. We just need some user info.
      if (process.env.VUE_APP_ENV === 'dev') {
        this.accessToken = { given_name: 'Wally User', realm_access: { roles: ['wally-view'] } }
        this.authenticated = true
        this.login()
        resolve()
        return
      }
      Axios.get('/oauth/token').then((r) => {
        this.accessToken = r.data
        this.authenticated = true
        this.login()
        resolve()
      }).error((e) => {
        reject(new Error('unable to initialize Keycloak'))
      })
    })
  }

  login (next) {
    this.name = this.accessToken['given_name']

    // required for allowing header to update the name.
    EventBus.$emit('auth:update', { name: this.name, authenticated: this.isAuthenticated() })
    if (next) {
      router.push(next)
    }
  }

  logout () {
    localStorage.removeItem('loggedIn')
    localStorage.removeItem('expiresAt')
    window.location.href = '/oauth/logout'
  }

  isAuthenticated () {
    return this.authenticated
  }

  hasRole (role) {
    return this.accessToken &&
    this.accessToken.realm_access &&
    this.accessToken.realm_access.roles &&
    ~this.accessToken.realm_access.roles.indexOf(role)
  }
}
