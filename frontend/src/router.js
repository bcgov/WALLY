import Vue from 'vue'
import Router from 'vue-router'
import Home from './components/common/Home.vue'
import Login from './views/Login.vue'
import Restricted from './views/Restricted.vue'

Vue.use(Router)

const guard = (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    if (!router.app.$auth.isAuthenticated()) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else if (!router.app.$auth.hasRole('wally-view')) {
      next({
        path: '/request-access'
      })
    } else {
      next()
    }
  } else {
    next() // make sure to always call next()!
  }
}

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/request-access',
      component: Restricted,
      name: 'request-access'
    }
  ]
})

router.beforeEach(guard)

export default router
