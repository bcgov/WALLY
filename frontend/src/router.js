import Vue from 'vue'
import Router from 'vue-router'

import LayerSelection from './components/sidebar/LayerSelection'
import SingleSelectedFeature from './components/sidebar/SingleSelectedFeature'
import MultipleSelectedFeatures from './components/sidebar/MultipleSelectedFeatures'

import Start from './components/sidebar/Start'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [

    {
      path: '/',
      name: 'home',
      component: Start,
      meta: {
        sidebarColumns: {
          md: 6,
          lg: 4,
          xl: 3
        }
      }
    },
    {
      path: '/layers',
      name: 'layer-selection',
      component: LayerSelection,
      meta: {
        sidebarColumns: {
          md: 6,
          lg: 4,
          xl: 3
        }
      }
    },
    {
      path: '/feature', // TODO: should refactor to be under /features/<feature_id>
      name: 'single-feature',
      component: SingleSelectedFeature,
      meta: {
        sidebarColumns: {
          md: 6,
          lg: 6,
          xl: 5
        }
      }
    },
    {
      path: '/features',
      name: 'multiple-features',
      component: MultipleSelectedFeatures,
      meta: {
        sidebarColumns: {}
      }
    }
  ]
})

export default router
