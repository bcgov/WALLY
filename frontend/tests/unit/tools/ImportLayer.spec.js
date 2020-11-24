import { shallowMount, createLocalVue } from '@vue/test-utils'
import ImportLayer from '../../../src/components/sidepanel/cards/ImportLayer.vue'
import FileList from '../../../src/components/tools/import_layer/FileList'

import Vuex from 'vuex'
import Vuetify from 'vuetify'
import Vue from 'vue'

const localVue = createLocalVue()
localVue.use(Vuex)
Vue.use(Vuetify)
const vuetify = new Vuetify()

global.config = {
  warnUploadFileSizeThresholdInMB: 10
}

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
    expect(wrapper.vm.determineFileType('test.geojson').fileType).toBe('geojson')
    expect(wrapper.vm.determineFileType('test.csv').fileType).toBe('csv')
    expect(wrapper.vm.determineFileType('test.kml').fileType).toBe('kml')
    expect(wrapper.vm.determineFileType('test.json').fileType).toBe('geojson')

    // future filetypes
    // expect(wrapper.vm.determineFileType('test.test.shp').type).toBe('shp')
    // expect(wrapper.vm.determineFileType('test.zip').type).toBe('shp')
    // expect(wrapper.vm.determineFileType('test.json').type).toBe('geojson')
  })

  it('Only accepts valid file types', async () => {
    wrapper.vm.fileList = []

    let testFile = new File([''],
      'test.txt',
      { type: 'text/plain' })

    wrapper.vm.readFile(testFile)
    await wrapper.vm.$nextTick()

    expect(wrapper.find('#statusMessage0').text().toLowerCase())
      .toContain('file of type txt not supported')
  })

  it('Displays an error message', async () => {
    wrapper.vm.handleFileMessage({
      message: 'test error message',
      status: 'error'
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.find('#statusMessage0').text().toLowerCase())
      .toContain('test error message')
  })

  it('Can load multiple files', async () => {
    wrapper.vm.readFiles = jest.fn()

    let testFile = new File([''], 'test.geojson', { type: 'application/geo+json' })
    let testFile2 = new File([''], 'test2.geojson', { type: 'application/geo+json' })

    wrapper.vm.loadFiles([testFile, testFile2])
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.readFiles).toHaveBeenCalled()
  })

  it('Hides FileDrop when processing files', async () => {
    wrapper.setData({
      fileList: [
        { name: 'test' }
      ]
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.find('filedrop-stub').exists()).toBeFalsy()
  })
})

describe('FileList', () => {
  let wrapper

  beforeEach(() => {
    let file = {
      size: 11 * 1024 * 1024 // 11mb
    }

    wrapper = shallowMount(FileList, {
      vuetify,
      localVue,
      propsData: {
        files: [file],
        fileLoading: []
      }
    })
  })

  it('Shows warning for files larger ' +
    'than the warning threshold', async () => {
    await wrapper.vm.$nextTick()

    expect(wrapper.find('#fileSizeWarning0').text().toLowerCase())
      .toContain('file size greater than 10 mb')
  })
})
