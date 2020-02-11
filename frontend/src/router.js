import Vue from 'vue'
import Router from 'vue-router'

import store from './store'

import LayerSelection from './components/toolbar/LayerSelection'
import SingleSelectedFeature from './components/sidepanel/SingleSelectedFeature'
import MultipleSelectedFeatures from './components/sidepanel/MultipleSelectedFeatures'
import PointOfInterest from './components/sidepanel/cards/PointOfInterest'
import PolygonTool from './components/sidepanel/cards/PolygonTool'
import CrossSectionContainer from './components/analysis/cross_section/CrossSectionContainer'
import StreamApportionmentContainer from './components/analysis/stream_apportionment/StreamApportionmentContainer'
import UpstreamDownstream from './components/sidepanel/cards/UpstreamDownstream'
import SurfaceWaterAnalysis from './components/sidepanel/cards/SurfaceWaterAnalysis'
import Start from './components/sidepanel/Start'
import WellsNearbyContainer from './components/analysis/wells_nearby/WellsNearbyContainer'
import WaterRightsLicencesNearbyContainer
  from './components/analysis/water_rights_licences_nearby/WaterRightsLicencesNearbyContainer'

Vue.use(Router)

const mapResize = (to, from, next) => {
  if (store.getters.map && store.getters.map.loaded()) {
    store.getters.map.resize()
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
      path: '/point-of-interest', // TODO: should refactor to be under
      // /features/<feature_id>
      name: 'point-of-interest',
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
      path: '/water-rights-licences-nearby', // TODO: should refactor to be
      // under
      // /features/<feature_id>
      name: 'water-rights-licences-nearby',
      component: WaterRightsLicencesNearbyContainer,
      meta: {
        sidebarColumns: {
          md: 6,
          lg: 6,
          xl: 5
        }
      }
    },
    {
      path: '/wells-nearby',
      name: 'wells-nearby',
      component: WellsNearbyContainer,
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
      component: CrossSectionContainer,
      meta: {
        sidebarColumns: {
          md: 6,
          lg: 6,
          xl: 5
        }
      }
    },
    {
      path: '/apportion-demand', // TODO: should refactor to be under /features/<feature_id>
      name: 'stream-apportionment',
      component: StreamApportionmentContainer,
      meta: {
        sidebarColumns: {
          md: 6,
          lg: 6,
          xl: 5
        }
      }
    },
    {
      path: '/upstream-downstream', // TODO: should refactor to be under /features/<feature_id>
      name: 'upstream-downstream',
      component: UpstreamDownstream,
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
    },
    {
      path: '/surface-water',
      name: 'surface-water',
      component: SurfaceWaterAnalysis,
      meta: {
        sidebarColumns: {}
      }
    }
  ]
})

router.afterEach(mapResize)
export default router
