import Vue from 'vue'
import Router from 'vue-router'

import mapStore from './store/mapStore'

import LayerSelection from './components/sidebar/LayerSelection'
import SingleSelectedFeature from './components/sidebar/SingleSelectedFeature'
import MultipleSelectedFeatures from './components/sidebar/MultipleSelectedFeatures'
import PointOfInterest from './components/sidebar/cards/PointOfInterest'
import PolygonTool from './components/sidebar/cards/PolygonTool'
import CrossSection from './components/sidebar/cards/CrossSection'
import Start from './components/sidebar/Start'

Vue.use(Router)

const mapResize = (to, from, next) => {
  if (mapStore.state.map && mapStore.state.map.loaded()) {
    mapStore.state.map.resize()
  }
}

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [

    {
      path: '/',
      name: 'home',
      component: Start,
      meta: {
        hide: true
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
      path: '/poi', // TODO: should refactor to be under /features/<feature_id>
      name: 'place-poi',
      component: PointOfInterest,
      meta: {
        sidebarColumns: {
          md: 6,
          lg: 6,
          xl: 5
        }
      }
    },
    {
      path: '/polygon', // TODO: should refactor to be under /features/<feature_id>
      name: 'polygon-tool',
      component: PolygonTool,
      meta: {
        sidebarColumns: {
          md: 6,
          lg: 6,
          xl: 5
        }
      }
    },
    {
      path: '/section', // TODO: should refactor to be under /features/<feature_id>
      name: 'cross-section',
      component: CrossSection,
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

router.afterEach(mapResize)
export default router
