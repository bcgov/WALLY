import { shallowMount, createLocalVue } from '@vue/test-utils'
import ImportLayer from '../../../src/components/sidepanel/cards/ImportLayer.vue'
import Vuex from 'vuex'
import Vuetify from 'vuetify'
import Vue from 'vue'

const localVue = createLocalVue()
localVue.use(Vuex)
Vue.use(Vuetify)
const vuetify = new Vuetify()

describe('ImportLayer', () => {
  let store
  let getters, mapGetters, customLayersGetters
  let wrapper
  let map
  let customLayers

  beforeEach(() => {
    mapGetters = {
      map: () => ({})
    }
    customLayersGetters = {
      selectedCustomLayers: () => ([]),
      customLayers: () => {}
    }
    map = {
      namespaced: true,
      getters: mapGetters
    }
    customLayers = {
      namespaced: true,
      getters: customLayersGetters
    }

    getters = {
      app: () => ({
        config: {
          'test prop': 'test value'
        }
      })

    }

    store = new Vuex.Store({ modules: { map, customLayers }, getters })

    store.dispatch = jest.fn()
    wrapper = shallowMount(ImportLayer, {
      vuetify,
      store,
      localVue
    })
  })

  it('determines filetype by extension', () => {
    expect(wrapper.vm.determineFileType('test.geojson')).toBe('geojson')
    expect(wrapper.vm.determineFileType('test.csv')).toBe('csv')
    expect(wrapper.vm.determineFileType('test.test.shp')).toBe('shp')
    expect(wrapper.vm.determineFileType('test.zip')).toBe('shp')
    expect(wrapper.vm.determineFileType('test.json')).toBe('geojson')
  })

  it('Only accepts valid file types', () => {
    wrapper.vm.fileList = []

    let testFile = new File([''],
      'test.geojson',
      { type: 'application/geo+json' })

    wrapper.vm.readFile(testFile)
    expect(wrapper.find('v-alert').html().toLowerCase())
      .toContain('unsupported file type')
  })

  it('Can load multiple files', () => {
    wrapper.vm.fileList = []
    let testFile = new File([''], 'test.geojson', { type: 'application/geo+json' })
    let testFile2 = new File([''], 'test2.geojson', { type: 'application/geo+json' })
    wrapper.vm.fileList = [testFile, testFile2]

    expect(wrapper.vm.readFiles).toHaveBeenCalled()
    expect(wrapper.vm.files.length).toBe(2)
  })

  it('Shows warning for files larger than 10mb', () => {
    expect(1).toEqual(1)
    let file = {
      stats: {
        size: 10 * 1e6
      }
    }
    wrapper.vm.files = [file]

    expect(wrapper.find('v-alert').html().toLowerCase())
      .toContain('file size greater than 10mb')
  })
})
