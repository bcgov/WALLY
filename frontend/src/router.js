import Vue from 'vue'
import Router from 'vue-router'
import Home from './components/Home.vue'
import Login from './views/Login.vue'
import Restricted from './views/Restricted.vue'

import LayerSelection from './components/sidebar/LayerSelection'
import SingleSelectedFeature from './components/sidebar/SingleSelectedFeature'
import Start from './components/sidebar/Start'

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
      },
      children: [
        {
          path: '/',
          name: 'start',
          component: Start
        },
        {
          path: '/layers',
          name: 'layer-selection',
          component: LayerSelection
        },
        {
          path: '/feature',
          name: 'single-feature',
          component: SingleSelectedFeature
        }
      ]
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
