import debounce from 'lodash.debounce'
import ApiService from '../services/ApiService'
import router from '../router'
import baseMapDescriptions from '../common/utils/baseMapDescriptions'
import HighlightPoint from '../components/map/MapHighlightPoint'
import area from '@turf/area'
import circle from '@turf/circle'
import length from '@turf/length'
import lineToPolygon from '@turf/line-to-polygon'
import pointInPolygon from '@turf/boolean-point-in-polygon'
import mapboxgl from 'mapbox-gl'
import MapboxDraw from '@mapbox/mapbox-gl-draw'
import qs from 'querystring'
import { wmsBaseURL } from '../common/utils/wmsUtils'
import MapScale from '../components/map/MapScale'
import { getDefaultStyle } from '../common/mapbox/styles'
import { addMapboxLayer } from '../common/utils/mapUtils'
import {
  geojsonFC,
  lineStringFeature,
  pointFeature,
  polygonFeature, vectorSource
} from '../common/mapbox/features'
import {
  highlightSources, measurementSources, SOURCE_CUSTOM_SHAPE_DATA,
  streamHighlightSources
} from '../common/mapbox/sourcesWally'

const emptyPoint = pointFeature([])
const emptyLine = lineStringFeature([])
const emptyPolygon = polygonFeature([[]])

const emptyFeatureCollection = {
  type: 'FeatureCollection',
  features: [emptyPoint]
}

const defaultMode = {
  type: 'interactive',
  name: 'clicky'
}

export default {
  namespaced: true,
  state: {
    map: null,
    isMapReady: false,
    draw: {},
    drawnMeasurements: null,
    geocoder: {},
    activeSelection: null,
    layerSelectTriggered: false,
    selectedMapLayerNames: [],
    activeMapLayers: [],
    mapLayers: [],
    highlightFeatureData: {},
    highlightFeatureCollectionData: {},
    layerCategories: [],
    layerSelectionActive: true,
    isDrawingToolActive: false,
    mode: defaultMode,
    drawPointOfInterest: false,
    selectedBaseLayers: [
      'national-park',
      'landuse',
      'contour-line',
      'hillshade'
    ],
    baseMapLayers: [{
      id: 'base-map-layers',
      name: 'Base Map Layers',
      children: baseMapDescriptions
    }]
  },
  actions: {
    async initMapAndDraw ({ commit, dispatch }) {
      const mapConfig = await ApiService.get('api/v1/config/map')
      mapboxgl.accessToken = mapConfig.data.mapbox_token

      const zoomConfig = {
        center: process.env.VUE_APP_MAP_CENTER ? JSON.parse(process.env.VUE_APP_MAP_CENTER) : [-124, 54.5],
        zoomLevel: process.env.VUE_APP_MAP_ZOOM_LEVEL ? process.env.VUE_APP_MAP_ZOOM_LEVEL : 4.7
      }

      let style = getDefaultStyle()

      global.config.debug && console.log('[wally] using style...', style)
      commit('setMap', new mapboxgl.Map({
        container: 'map', // container id
        style,
        center: zoomConfig.center, // starting position
        zoom: zoomConfig.zoomLevel, // starting zoom
        attributionControl: false, // hide default and re-add to the top left
        preserveDrawingBuffer: true, // allows image export of the map at
        // the cost of some performance
        trackResize: true
      }))

      const modes = MapboxDraw.modes
      modes.simple_select.onTrash = this.clearSelections
      modes.draw_polygon.onTrash = this.clearSelections
      modes.draw_line_string.onTrash = this.clearSelections
      modes.draw_point.onTrash = this.clearSelections
      modes.direct_select.onTrash = this.clearSelections

      commit('setDraw', new MapboxDraw({
        modes: modes,
        displayControlsDefault: false,
        controls: {
          // polygon: true,
          // point: true,
          // line_string: true,
          // trash: true
        }
      }))

      // Fix for the map not expanding to full size when you resize the
      // browser window
      window.addEventListener('resize', () => {
        dispatch('resizeMap')
      })
    },
    resizeMap ({ state }) {
      // MapboxGL's resize function gets the canvas container div's dimensions
      // and repaints the canvas accordingly.
      // https://github.com/mapbox/mapbox-gl-js/blob/0412fdb247f0f0c0bdb46d1e1465a848e1eea7dc/src/ui/map.js#L558

      // Get the map's parent node height and set the canvas container to
      // the same height
      const mapboxglCanvasContainer = document.getElementsByClassName('mapboxgl-canvas-container')[0]
      const map = document.getElementById('map')
      mapboxglCanvasContainer.style.height = getComputedStyle(map.parentNode).height

      const infoSheetWidth = document.getElementById('info-sheet')
        ? getComputedStyle(document.getElementById('info-sheet')).width
        : 0
      mapboxglCanvasContainer.style.width = window.innerWidth - infoSheetWidth

      // Mapbox resize takes some time to get the updated height, so it
      // only works when you wait a bit.
      // TODO: reconsider this setTimeout
      setTimeout(() => {
        state.map.resize()
      }, 300)
    },
    loadMap ({ state, dispatch }) {
      state.map.on('style.load', () => {
        dispatch('getMapLayers')
        dispatch('initStreamHighlights')
      })
    },
    setDrawMode ({ state }, drawMode) {
      if (state.draw && state.draw.changeMode) {
        state.isDrawingToolActive = drawMode !== 'simple_select'
        state.draw.changeMode(drawMode)
      }
    },
    addFeaturePOIFromCoordinates ({ state, dispatch, commit }, data) {
      const point = {
        type: 'Feature',
        id: 'point_of_interest',
        geometry: {
          display_data_name: data.layerName,
          type: 'Point',
          coordinates: data.coordinates
        },
        display_data_name: data.layerName,
        properties: {
        }
      }
      commit('setDrawPointOfInterest', true)
      dispatch('addSelectedFeature', point)
    },
    async addSelectedFeature ({ state, dispatch }, feature) {
      if (!state.isMapReady) {
        return
      }

      state.draw.add(feature)
      dispatch('addActiveSelection', { featureCollection: { features: [feature] } })
    },
    selectPointOfInterest ({ commit, dispatch }) {
      commit('setDrawPointOfInterest', true)
      dispatch('setDrawMode', 'draw_point')
    },
    addActiveSelection ({ commit, dispatch, state }, { featureCollection, options = {} }) {
      // options:
      // alwaysReplaceFeatures: indicates that features should always be cleared (even if
      // there are no new features to replace them).  Toggling this is useful for
      // changing the behavior of mouse clicks (which probably should not clear
      // features without warning) vs explicitly searching for features in an area.
      // (which would be expected to clear features from a previous search area).
      //
      // showFeatureList: (deprecated) indicates whether to switch the screen to the feature
      // list. Setting to false is for preventing switching screens while doing other tasks e.g.
      // changing layers (which triggers a new search with the new layer included). Made
      // redundant by separating the layer select screen and feature views.

      // console.log('active selection - - ', state.isDrawingToolActive)
      // if (state.isDrawingToolActive) {
      //   return false
      // }

      const defaultOptions = {
        showFeatureList: true,
        alwaysReplaceFeatures: false
      }

      options = Object.assign({}, defaultOptions, options)

      // console.log(options)

      if (!featureCollection || !featureCollection.features || !featureCollection.features.length) return

      if (options.showFeatureList) {
        commit('setLayerSelectionActiveState', false)
      }

      const newFeature = featureCollection.features[0]
      commit('replaceOldFeatures', newFeature.id)

      // Active selection is a Point, and we're drawing a point of interest
      if (newFeature.geometry.type === 'Point' && state.drawPointOfInterest) {
        newFeature.display_data_name = 'point_of_interest'
        commit('setDrawPointOfInterest', false)
        commit('setPointOfInterest', newFeature, { root: true })
        return
      }

      // Active selection is a LineString
      if (newFeature.geometry.type === 'LineString') {
        newFeature.display_data_name = 'user_defined_line'
        commit('setSectionLine', newFeature, { root: true })
        return
      }

      global.config.debug && console.log('[wally] feature : ', newFeature)

      // for drawn rectangular regions, the polygon describing the rectangle is the first
      // element in the array of drawn features.
      // note: this is what might break if extending the selection tools to draw more objects.
      dispatch('handleGetMapObjects', { bounds: newFeature, options: { alwaysReplaceFeatures: options.alwaysReplaceFeatures } })
      commit('setSelectionBoundingBox', newFeature, { root: true })
    },
    updateActiveMapLayers ({ commit, state, dispatch }, selectedLayers) {
      // accepts an array of layer names and sets the active map layers accordingly
      state.selectedMapLayerNames = selectedLayers

      // list of prev layers.  the payload is the new list of layers about to be active.
      const prev = state.activeMapLayers.map(l => l.display_data_name)

      // get list of layers that were deselected (they were in `prev`, but are not in payload),
      // and sent an event to remove them.
      prev.filter((l) => !selectedLayers.includes(l)).forEach((l) => {
        dispatch('removeMapLayer', l)
        if (l === 'water_licensed_works') {
          for (let i = 1; i < 5; i++) {
            commit('deactivateLayer', 'water_licensed_works_dash' + i)
          }
        }
      })

      // similarly, now get a list of layers that are in payload but weren't in the previous active layers.
      selectedLayers.filter((l) => !prev.includes(l)).forEach((l) => {
        // Customized Metrics - Track when a layer is selected
        const layerName = state.mapLayers.find(e => e.display_data_name === l).display_name
        window._paq && window._paq.push(['trackEvent', 'Layer', 'Activate Layer', layerName])
        commit('activateLayer', l)
        if (l === 'water_licensed_works') {
          for (let i = 1; i < 5; i++) {
            commit('activateLayer', 'water_licensed_works_dash' + i)
          }
        }
      })

      // reset the list of active layers
      commit('setActiveMapLayers', selectedLayers)

      // redraw any current features and update selection.
      dispatch('addActiveSelection', { featureCollection: state.draw.getAll(), options: { showFeatureList: false } })
    },
    addMapLayer ({ commit, dispatch, state }, displayDataName) {
      let mapLayer = state.mapLayers.find((layer) => {
        return layer.display_data_name === displayDataName
      })

      // mapLayer may be undefined if it wasn't found in the list of
      // map layers (for example, addMapLayer was called before the layer
      // catalogue loaded or was called with an unexpected layer).  If so,
      // stop here.
      if (!mapLayer) {
        return
      }

      if (!state.activeMapLayers.includes(mapLayer)) {
        state.activeMapLayers.push(mapLayer)
        commit('activateLayer', displayDataName)
      }
    },
    removeMapLayer ({ state, dispatch, commit }, payload) {
      state.activeMapLayers = state.activeMapLayers.filter((layer) => {
        return layer.display_data_name !== payload
      })
      dispatch('clearHighlightLayer')
      commit('deactivateLayer', payload)
    },
    async getMapLayers ({ state, commit, dispatch }) {
      // We only fetch maplayers if we don't have a copy cached
      if (state.mapLayers === undefined || state.mapLayers.length === 0) {
        return new Promise((resolve, reject) => {
          ApiService.getApi('/catalogue/all')
            .then((response) => {
              commit('setMapLayers', response.data.layers)
              commit('setLayerCategories', response.data.categories)
              dispatch('initHighlightLayers')
              dispatch('initMeasurementHighlight')
              commit('initVectorLayerSources', response.data.layers)
            })
            .catch((error) => {
              reject(error)
            })
        })
      }
    },
    handleGetMapObjects:
      debounce(async function ({ dispatch }, { bounds, options }) {
        dispatch('getMapObjects', { bounds, options })
      }, 1000),
    async getMapObjects ({ commit, dispatch, state, getters }, { bounds, options = {} }) {
      // TODO: Separate activeMaplayers by activeWMSLayers and activeDataMartLayers
      // options:
      // alwaysReplaceFeatures: indicates that features should always be cleared (even if
      // there are no new features to replace them).  Toggling this is useful for
      // changing the behavior of mouse clicks (which probably should not clear
      // features without warning) vs explicitly searching for features in an area.
      // (which would be expected to clear features from a previous search area).

      const defaultOptions = {
        alwaysReplaceFeatures: false
      }

      options = Object.assign({}, defaultOptions, options)

      global.config.debug && console.log('[wally] map click')
      // const popup = new mapboxgl.Popup({
      //   closeButton: false,
      //   closeOnClick: false
      // })
      // Return if we're in "analyze mode"
      if (state.mode.type === 'interactive') {
        const canvas = await state.map.getCanvas()
        const size = { x: canvas.width, y: canvas.height }

        global.config.debug && console.log('[wally] discard features before' +
          ' querying: ', options.alwaysReplaceFeatures)

        if (options.alwaysReplaceFeatures) {
          commit('clearDataMartFeatures', {}, { root: true })
        }
        commit('replaceOldFeatures', bounds.id)
        global.config.debug && console.log('[wally]', bounds)

        dispatch('getDataMartFeatures', {
          bounds: bounds,
          size: size,
          layers: state.activeMapLayers
        }, { root: true })
      }
    },
    clearSelections ({ state, commit, dispatch }) {
      dispatch('clearHighlightLayer')
      commit('replaceOldFeatures')
      commit('clearMeasurements')
      dispatch('clearMeasurementHighlights')
      commit('clearDataMartFeatures', {}, { root: true })
      commit('removeShapes')
      commit('resetPointOfInterest', {}, { root: true })
      commit('resetDataMartFeatureInfo', {}, { root: true })
    },
    clearHighlightLayer ({ commit, state, dispatch }) {
      if (!state.isMapReady) {
        return
      }

      const pointData = state.map.getSource('highlightPointData')
      const layerData = state.map.getSource('highlightLayerData')

      if (pointData) {
        pointData.setData(emptyPoint)
      }

      if (layerData) {
        layerData.setData(emptyPolygon)
      }
      dispatch('removeElementsByClass', 'annotationMarker')
      dispatch('clearStreamHighlights')
      commit('resetStreamData', {}, { root: true })
    },
    clearStreamHighlights ({ rootGetters, state }) {
      streamHighlightSources.forEach((source) => {
        state.map.getSource(source).setData(emptyFeatureCollection)
      })
    },
    setActiveBaseMapLayers ({ state, commit }, payload) {
      let prev = state.selectedBaseLayers
      prev.filter((l) => !payload.includes(l)).forEach((l) => commit('deactivateBaseLayer', l))
      payload.filter((l) => !prev.includes(l)).forEach((l) => commit('activateBaseLayer', l))
      state.selectedBaseLayers = payload
    },
    initStreamHighlights ({ state, rootGetters }) {
      // Import sources and layers for stream segment highlighting
      streamHighlightSources.forEach((source) => {
        state.map.addSource(source, geojsonFC(emptyFeatureCollection))
        addMapboxLayer(state.map, source, {})
      })
    },
    async initHighlightLayers ({ state, commit }) {
      await state.map.on('load', () => {
        // initialize highlight layers
        state.map.addImage('highlight-point', HighlightPoint(state.map, 90), { pixelRatio: 2 })
        highlightSources.forEach((source) => {
          console.log('hl layers', source, source.includes('Point'))
          const defaultData = source.includes('Point') ? emptyPoint : emptyPolygon
          state.map.addSource(source, geojsonFC(defaultData))
          addMapboxLayer(state.map, source, {})
        })

        global.config.debug && console.log('[wally] map is now ready')
        // End of cascade; map is now ready
        commit('setInfoPanelVisibility', true, { root: true })
        commit('setMapReady', true)
      })
    },
    updateMapLayerData ({ state, commit, dispatch }, data) {
      let { source, featureData } = data
      state.map.getSource(source).setData(featureData)
    },
    /*
      Highlights a single Feature dataset
     */
    updateHighlightLayerData ({ state, commit, dispatch }, data) {
      // For stream networks layer we add custom highlighting and reset poly/point highlight layering
      if (data.display_data_name === 'freshwater_atlas_stream_networks') {
        state.map.getSource('highlightPointData').setData(emptyPoint)
        state.map.getSource('highlightLayerData').setData(emptyPolygon)
        // For local rendered streams only calculation

        // Backend query for all connected streams
        // this.$store.dispatch('fetchConnectedStreams', { stream: data })
      } else if (data.geometry.type === 'Point') { // Normal poly/point highlighting
        state.map.getSource('highlightPointData').setData(data)
        state.map.getSource('highlightLayerData').setData(emptyPolygon)
      } else {
        state.map.getSource('highlightPointData').setData(emptyPoint)
        state.map.getSource('highlightLayerData').setData(data)
      }
    },
    removeElementsByClass ({ state }, payload) {
      let elements = document.getElementsByClassName(payload)
      while (elements.length > 0) {
        elements[0].parentNode.removeChild(elements[0])
      }
    },
    async initMeasurementHighlight ({ state }, payload) {
      await state.map.on('load', () => {
        // initialize measurement highlight layer
        measurementSources.forEach((source) => {
          state.map.addSource(source, geojsonFC(emptyPolygon))
          addMapboxLayer(state.map, source, {})
        })
      })
    },
    updateMeasurementHighlight ({ state, commit, dispatch }, data) {
      if (data.feature.geometry.type === 'LineString') {
        state.map.getSource('measurementPolygonHighlight').setData(emptyPolygon)
        state.map.getSource('measurementSnapCircle').setData(data.snapPoint)
        state.map.getSource('measurementLineHighlight').setData(data.feature)
      } else {
        state.map.getSource('measurementPolygonHighlight').setData(data.feature)
        state.map.getSource('measurementSnapCircle').setData(emptyPolygon)
        state.map.getSource('measurementLineHighlight').setData(emptyLine)
      }
    },
    clearMeasurementHighlights ({ state }, payload) {
      state.map.getSource('measurementPolygonHighlight').setData(emptyPolygon)
      state.map.getSource('measurementSnapCircle').setData(emptyPolygon)
      state.map.getSource('measurementLineHighlight').setData(emptyLine)
    }
  },
  mutations: {
    activateLayer (state, displayDataName) {
      state.map.setLayoutProperty(displayDataName, 'visibility', 'visible')
    },
    deactivateLayer (state, displayDataName) {
      state.map.setLayoutProperty(displayDataName, 'visibility', 'none')
    },
    activateBaseLayer (state, layerId) {
      state.map.setLayoutProperty(layerId, 'visibility', 'visible')
    },
    deactivateBaseLayer (state, layerId) {
      state.map.setLayoutProperty(layerId, 'visibility', 'none')
    },
    removeLayer (state, layerId) {
      state.map.removeLayer(layerId)
    },
    setDrawToolInActive (state) {
      setTimeout(() => { // delay to let other draw actions finish
        state.isDrawingToolActive = false
      }, 500)
    },
    initVectorLayerSources (state, allLayers) {
      allLayers.forEach((layer) => {
        if (layer.use_wms) {
          const sourceID = layer.source_layer
          const layerID = layer.display_data_name
          const wmsOpts = {
            service: 'WMS',
            request: 'GetMap',
            format: 'application/x-protobuf;type=mapbox-vector',
            layers: 'pub:' + layer.wms_name,
            styles: layer.wms_style,
            transparent: true,
            name: layer.display_name,
            height: 256,
            width: 256,
            overlay: true,
            srs: 'EPSG:3857'
          }
          const query = qs.stringify(wmsOpts)
          let url = wmsBaseURL + layer.wms_name + '/ows?' + query + '&BBOX={bbox-epsg-3857}'
          // GWELLS specific url because we get vector tiles directly from the GWELLS DB, not DataBC
          if (sourceID === 'groundwater_wells' || sourceID === 'aquifers') {
            url = `https://apps.nrs.gov.bc.ca/gwells/tiles/${layer.wms_name}/{z}/{x}/{y}.pbf`
          }
          if (!state.map.getSource(sourceID)) {
            state.map.addSource(sourceID, vectorSource(url, sourceID))
          }
          addMapboxLayer(state.map, layerID, { sourceLayer: layer.wms_name })
        }
      })
    },
    addShape (state, shape) {
      // adds a mapbox-gl-draw shape to the map
      state.map.getSource(SOURCE_CUSTOM_SHAPE_DATA).setData(shape)
    },
    removeShapes (state) {
      state.map.getSource(SOURCE_CUSTOM_SHAPE_DATA).setData(emptyPolygon)
    },
    replaceOldFeatures (state, newFeature = null) {
      // replace all previously drawn features with the new one.
      // this has the effect of only allowing one selection box to be drawn at a time.
      const old = state.draw.getAll().features.filter((f) => f.id !== newFeature)
      state.draw.delete(old.map((feature) => feature.id))
    },
    setMap (state, payload) {
      state.map = payload
    },
    setDraw (state, payload) {
      state.draw = payload
    },
    setGeocoder (state, payload) {
      state.geocoder = payload
    },
    setLayerSelectTriggered (state, payload) {
      state.layerSelectTriggered = payload
    },
    setLayerSelectionActiveState (state, payload) {
      state.layerSelectionActive = payload
    },
    setLayerCategories (state, payload) {
      state.layerCategories = payload
    },
    setActiveMapLayers (state, payload) {
      state.activeMapLayers = state.mapLayers.filter((l) => {
        return payload.includes(l.display_data_name)
      })
    },
    setMapLayers (state, payload) {
      state.mapLayers = payload
    },
    updateHighlightFeatureData (state, payload) {
      state.highlightFeatureData = payload
    },
    updateHighlightFeatureCollectionData (state, payload) {
      state.highlightFeatureCollectionData = payload
    },
    setCursorPointer (state) {
      state.map.getCanvas().style.cursor = 'pointer'
    },
    resetCursor (state) {
      state.map.getCanvas().style.cursor = ''
    },
    setMapReady (state, payload) {
      state.isMapReady = payload
    },
    setMode (state, payload) {
      state.mode = payload
    },
    setDrawPointOfInterest (state, payload) {
      state.drawPointOfInterest = payload
    },
    resetMode (state, payload) {
      state.mode = defaultMode
    },
    handleMeasurements (state, payload) {
      if (router.currentRoute.name !== 'measuring-tool') {
        return
      }

      const features = state.draw.getAll().features

      if (features.length > 0) {
        const feature = features[0]
        const drawnLength = (length(feature) * 1000) // meters
        const coordinates = feature.geometry.coordinates

        // Calculate if last click point is close to the first click point
        // to determine whether to draw a line or an area.
        const scale = MapScale(state.map)
        const radius = scale / 1000 * 0.065 // scale radius based on map zoom level
        const options = { steps: 10, units: 'kilometers', properties: {} }
        const bounds = circle(coordinates[0], radius, options)
        const lineConnects = pointInPolygon(coordinates[coordinates.length - 1], bounds)

        // metric calculations
        let drawnMeasurements = {}

        // calculate area and perimeter and highlight polygon shape
        if (coordinates.length > 3 && lineConnects) {
          // set last coordinate equal to the first
          // because the click point is within the minimum bounds
          let lineFeature = feature
          let ac = lineFeature.geometry.coordinates
          ac[ac.length - 1] = ac[0]
          lineFeature.geometry.coordinates = ac
          let perimeterMeasurement = (length(lineFeature) * 1000)

          // update draw feature collection with connected lines
          state.draw.set({
            type: 'FeatureCollection',
            features: [{
              type: 'Feature',
              properties: {},
              id: feature.id,
              geometry: lineFeature.geometry
            }]
          })

          let areaUnits = 'm²'
          let perimeterUnits = 'm'
          let polygonFeature = lineToPolygon(lineFeature)
          let areaMeasurement = area(polygonFeature)

          if (perimeterMeasurement >= 1000) { // if over 1000 meters, upgrade metric
            perimeterMeasurement = perimeterMeasurement / 1000
            perimeterUnits = 'km'
          }
          if (areaMeasurement >= 100000) { // if over 100,000 meters, upgrade metric
            areaMeasurement = areaMeasurement / 1000000
            areaUnits = 'km²'
          }

          drawnMeasurements = {
            features: features,
            feature: polygonFeature,
            perimeter: `${perimeterMeasurement.toFixed(2)} ${perimeterUnits}`,
            area: `${areaMeasurement.toFixed(2)} ${areaUnits}`
          }
        // calculate line distance and highlight line shape
        } else {
          let distanceUnits = 'm'
          let distance = drawnLength

          if (distance >= 1000) { // if over 1000 meters, upgrade metric
            distance = distance / 1000
            distanceUnits = 'km'
          }

          drawnMeasurements = {
            features: features,
            feature: feature,
            snapPoint: bounds,
            distance: `${distance.toFixed(2)} ${distanceUnits}`
          }
        }
        state.drawnMeasurements = drawnMeasurements
      }
    },
    clearMeasurements (state, payload) {
      state.drawnMeasurements = null
    }
  },
  getters: {
    selectedMapLayerNames: state => state.selectedMapLayerNames,
    activeMapLayers: state => state.activeMapLayers,
    isMapLayerActive: state => displayDataName => !!state.activeMapLayers.find((x) => x && x.display_data_name === displayDataName),
    isMapReady: state => state.isMapReady,
    isDrawingToolActive: state => state.isDrawingToolActive,
    mapLayerName: (state) => (wmsName) => {
      let layer = state.mapLayers.find(e => e.wms_name === wmsName)
      return layer ? layer.display_name : ''
    },
    getMapLayer: (state) => (displayDataName) => {
      let layer = state.mapLayers.find(e => e.display_data_name === displayDataName)
      return layer || null
    },
    allMapLayers: state => state.mapLayers,
    highlightFeatureData: state => state.highlightFeatureData,
    highlightFeatureCollectionData: state => state.highlightFeatureCollectionData,
    getCategories: state => state.layerCategories,
    layerSelectionActive: state => state.layerSelectionActive,
    selectedBaseLayers: state => state.selectedBaseLayers,
    baseMapLayers: state => state.baseMapLayers,
    map: state => state.map,
    draw: state => state.draw,
    geocoder: state => state.geocoder,
    layerSelectTriggered: state => state.layerSelectTriggered,
    drawnMeasurements: state => state.drawnMeasurements
  }
}
