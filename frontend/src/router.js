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
import FirstNationsAreasNearbyContainer
  from './components/analysis/first_nations_areas_nearby/FirstNationsAreasNearbyContainer'

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
        title: `Layers - ${global.config.title}`,
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
        title: `Feature - ${global.config.title}`,
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
        title: `Point of Interest - ${global.config.title}`,
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
        title: `Water Rights Licences Nearby - ${global.config.title}`,
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
        title: `Wells Nearby - ${global.config.title}`,
        sidebarColumns: {
          md: 6,
          lg: 6,
          xl: 5
        }
      }
    },
    {
      path: '/first-nations-areas-nearby',
      name: 'first-nations-areas-nearby',
      component: FirstNationsAreasNearbyContainer,
      meta: {
        title: `First Nations Areas Nearby - ${global.config.title}`,
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
        title: `Polygon Selection - ${global.config.title}`,
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
        title: `Cross Section - ${global.config.title}`,
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
        title: `Stream Apportionment - ${global.config.title}`,
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
        title: `Upstream and Downstream - ${global.config.title}`,
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
        title: `Multiple Selected Features - ${global.config.title}`,
        sidebarColumns: {}
      }
    },
    {
      path: '/surface-water',
      name: 'surface-water',
      component: SurfaceWaterAnalysis,
      meta: {
        title: `Surface Water Analysis - ${global.config.title}`,
        sidebarColumns: {}
      }
    },
    {
      path: '/oauth/logout',
      redirect: 'https://logontest.gov.bc.ca/clp-cgi/logoff.cgi'
    }
  ]
})

router.afterEach(mapResize)
// https://github.com/AmazingDreams/vue-matomo/issues/60
// vue-matomo currently doesn't track the URL, just the page title from the
// router. Until the issue above is fixed, we can report the URL change to
// matomo in this manner
router.afterEach((to, from) => {
  Vue.nextTick(() => {
    // Change the page title in the browser
    document.title = to.meta.title ? to.meta.title : global.config.title

    window._paq.push(['setReferrerUrl', from.fullPath])
    window._paq.push(['setCustomUrl', to.fullPath])
  })
})
export default router
