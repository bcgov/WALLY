import ApiService from './ApiService.js'
import Vue from 'Vue'
import EventBus from './EventBus.js'

const kcConfig = {
  realm: 'gwells',
  authServer: 'https://sso-test.pathfinder.gov.bc.ca/auth',
  sslRequired:	'external',
  resource:	'wally-test',
  publicClient: true,
  confidentialPort: 0,
  clientId: 'wally-test',
}

export class AuthService {
  kc = 'keycloak'

  accessToken
  idToken
  expiresAt
  name
  authenticated = this.kc.authenticated

  login (next) {
    // check for logged-in hint kept in localStorage.
    // this helps skip a step if it's likely that the user still
    // has a valid session with the SSO service.
    const loggedIn = JSON.parse(localStorage.getItem('loggedIn'))
    const expiresAt = JSON.parse(localStorage.getItem('expiresAt'))


    if (loggedIn && expiresAt) {

      // try renewing the session.  This has the effect of providing a new access
      // token, even if the client currently does not have one, as long as the user
      // still has a valid SSO session.
      this.renewSession().then(() => {

        // if a 'next' route was provided, send user there after successfully authenticating.
        // otherwise, they should arrive at the home screen.
        if (next) {
          router.push(next)
        } else {
          router.push({ name: 'home' })
        }
        EventBus.$emit('authChange', { authenticated: true })
      }).catch((e) => {
        // session could not be renewed, start normal login process.
        this.logout()
        this.kc.login()
      })
    } else {
      this.kc.login()
    }
  }
  logout () {
    localStorage.removeItem('loggedIn')
    localStorage.removeItem('expiresAt')
    this.kc.clearToken()
  }

  renewSession (ifExpiresIn = 3600) {
    return new Promise((resolve, reject) => {
      this.kc.updateToken(ifExpiresIn).success((r) => {
        if (r) {
          // successfully refreshed
          console.log('refreshed')
        } else {
          // unsuccessful
        }
      })
    })
  }
}
