import Vue from 'vue'
import Router from 'vue-router'

import store from './store'

import LayerSelection from './components/toolbar/LayerSelection'
import SingleSelectedFeature from './components/sidepanel/SingleSelectedFeature'
import MultipleSelectedFeatures from './components/sidepanel/MultipleSelectedFeatures'
import PointOfInterest from './components/sidepanel/cards/PointOfInterest'
import PolygonTool from './components/sidepanel/cards/PolygonTool'
import MeasuringTool from './components/sidepanel/cards/MeasuringTool'
import CrossSectionContainer from './components/analysis/cross_section/CrossSectionContainer'
import HydraulicConnectivityContainer from './components/analysis/hydraulic_connectivity/HydraulicConnectivityContainer'
import UpstreamDownstream from './components/analysis/upstream_downstream/UpstreamDownstreamContainer'
import SurfaceWaterContainer from './components/analysis/surface_water/SurfaceWaterContainer'
import Start from './components/sidepanel/Start'
import WellsNearbyContainer from './components/analysis/wells_nearby/WellsNearbyContainer'
import WaterRightsLicencesNearbyContainer from './components/analysis/water_rights_licences_nearby/WaterRightsLicencesNearbyContainer'
import FirstNationsAreasNearbyContainer from './components/analysis/first_nations_areas_nearby/FirstNationsAreasNearbyContainer'
import ImportLayer from './components/sidepanel/cards/ImportLayer'
import ProjectList from './components/projects/ProjectList'
import SavedAnalysesList from './components/savedanalyses/SavedAnalysesList'

Vue.use(Router)

const mapResize = (to, from, next) => {
  if (store.getters.map && store.getters.map.loaded()) {
    store.getters.map.resize()
  }
}

const title = global ? global.config ? global.config.title : '' : ''

// route meta options:
// hide:            routes with the `hide` flag default to starting with the sidebar hidden.
//                  default: false
// allowRedirect:   allows user interactions like map clicks to redirect off this route.
//                  e.g.: clicking on features should redirect away from the 'home' route to display
//                  information about that feature, but not from the surface water analysis routes.
//                  default: false
// sidebarColumns:  indicates how many columns by default a sidebar feature should be allowed
//                  to occupy.  todo: check that this is used consistently before relying on it.
const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Start,
      meta: {
        hide: true,
        allowRedirect: true
      }
    },
    {
      path: '/layers',
      name: 'layer-selection',
      component: LayerSelection,
      meta: {
        title: `Layers - ${title}`,
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
        title: `Feature - ${title}`,
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
        title: `Point of Interest - ${title}`,
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
        title: `Water Rights Licences Nearby - ${title}`,
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
        title: `Wells Nearby - ${title}`,
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
        title: `First Nations Areas Nearby - ${title}`,
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
        title: `Polygon Selection - ${title}`,
        sidebarColumns: {
          md: 6,
          lg: 6,
          xl: 5
        }
      }
    },
    {
      path: '/measuring',
      name: 'measuring-tool',
      component: MeasuringTool,
      meta: {
        title: `Measuring - ${title}`,
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
        title: `Cross Section - ${title}`,
        sidebarColumns: {
          md: 6,
          lg: 6,
          xl: 5
        }
      }
    },
    {
      // Retired path; 'apportion' is now is "assign demand"
      path: '/apportion-demand',
      redirect: '/assign-demand'
    },
    {
      path: '/assign-demand',
      name: 'hydraulic-connectivity',
      component: HydraulicConnectivityContainer,
      meta: {
        title: `Hydraulic Connectivity Analysis - ${title}`,
        sidebarColumns: {
          md: 6,
          lg: 6,
          xl: 5
        }
      }
    },
    {
      path: '/upstream-downstream',
      name: 'upstream-downstream',
      component: UpstreamDownstream,
      meta: {
        title: `Upstream and Downstream - ${title}`,
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
        title: `Multiple Selected Features - ${title}`,
        sidebarColumns: {},
        allowRedirect: true
      }
    },
    {
      path: '/surface-water',
      name: 'surface-water',
      component: SurfaceWaterContainer,
      meta: {
        title: `Surface Water Analysis - ${title}`,
        sidebarColumns: {}
      }
    },
    {
      path: '/import-data-layer',
      name: 'import-data-layer',
      component: ImportLayer,
      meta: {
        title: `Import File - ${title}`,
        sidebarColumns: {},
        allowRedirect: true
      }
    },
    {
      path: '/projects',
      name: 'projects',
      component: ProjectList
    },
    {
      path: '/saved-analyses',
      name: 'saved-analyses',
      component: SavedAnalysesList
    }
  ]
})

router.beforeEach((to, from, next) => {
  // Check if feature is enabled
  if (to.name === 'import-data-layer' &&
    store.getters.app &&
    store.getters.app.config &&
    !store.getters.app.config.external_import) next({ name: 'home' })
  else next()
})

router.afterEach(mapResize)
// https://github.com/AmazingDreams/vue-matomo/issues/60
// vue-matomo currently doesn't track the URL, just the page title from the
// router. Until the issue above is fixed, we can report the URL change to
// matomo in this manner
router.afterEach((to, from) => {
  Vue.nextTick(() => {
    // Change the page title in the browser
    document.title = to.meta.title ? to.meta.title : title

    window._paq && window._paq.push(['setReferrerUrl', from.fullPath])
    window._paq && window._paq.push(['setCustomUrl', to.fullPath])
  })
})
export default router
