import Vue from 'vue'
import Router from 'vue-router'
import Home from './components/common/Home.vue'
import Login from './views/Login.vue'
import Restricted from './views/Restricted.vue'
import LayerSelection from './components/layer_selection/LayerSelection.vue'
import MapFeatureSelectionSingle from './components/panels/MapFeatureSelectionSingle'
import Analysis from './components/analysis/Analysis'
import WellsByDistance from './components/analysis/WellsByDistance.vue'
import Chart from './components/charts/Chart'
import MapFeatureSelection from './components/panels/MapFeatureSelection'

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
      // redirect: '/map-layers',
      name: 'home',
      component: Home,
      meta: {
        requiresAuth: true
      },
      children: [
        {
          path: 'map-layers',
          component: LayerSelection
        },
        {
          path: 'map-info',
          component: MapFeatureSelection// Panel - Info - containing Single
          // selection or
          // multi
          // select
        },
        {
          path: 'analysis',
          component: Analysis,
          children: [
            {
              path: 'wells-by-distance/:coordinates',
              component: WellsByDistance,
              props: true
            }
          ]
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
