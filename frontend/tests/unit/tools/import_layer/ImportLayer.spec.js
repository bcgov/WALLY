import { shallowMount, createLocalVue } from '@vue/test-utils'
import ImportLayer from '../../../../src/components/sidepanel/cards/ImportLayer.vue'
import FileList from '../../../../src/components/tools/import_layer/FileList'

import Importer from '../../../../src/common/utils/Importer'

import Vuex from 'vuex'
import Vuetify from 'vuetify'
import Vue from 'vue'
import FileListProcessed
  from '../../../../src/components/tools/import_layer/FileListProcessed'

const localVue = createLocalVue()
localVue.use(Vuex)
Vue.use(Vuetify)
const vuetify = new Vuetify()

global.config = {
  warnUploadFileSizeThresholdInMB: 10
}

let getters, mapGetters, customLayersGetters
let map, importer
let customLayers

const initStore = ({ queuedFiles = [], processedFiles = [], loadingFiles = [] }) => {
  let store
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

  importer = {
    namespaced: true,
    getters: {
      queuedFiles: () => queuedFiles,
      processedFiles: () => processedFiles,
      isFileLoading: () => jest.fn(x => false)
    },
    mutations: {
      clearAllFiles: jest.fn()
    },
    actions: {
    }
  }

  getters = {
    app: () => ({
      config: {
        'test prop': 'test value'
      }
    })

  }

  store = new Vuex.Store({
    modules: { map, customLayers, importer },
    getters
  })

  store.dispatch = jest.fn()

  return store
}

describe('ImportLayer', () => {
  let store
  let wrapper

  const initComponent = ({ queuedFiles = [], processedFiles = [], loadingFiles = [] }) => {
    store = initStore({ queuedFiles, processedFiles, loadingFiles })
    wrapper = shallowMount(ImportLayer, {
      vuetify,
      store,
      localVue
    })
  }

  it('Can load multiple files', async () => {
    initComponent({})

    Importer.readFiles = jest.fn()
    wrapper.vm.clearAllFiles = jest.fn()

    const testFile = new File([''], 'test.geojson', { type: 'application/geo+json' })
    const testFile2 = new File([''], 'test2.geojson', { type: 'application/geo+json' })

    wrapper.vm.handleSelectedFiles([testFile, testFile2])
    wrapper.vm.prepareFiles()
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.clearAllFiles).toHaveBeenCalled()
    expect(Importer.readFiles).toHaveBeenCalledWith([testFile, testFile2])
  })

  it('Hides FileDrop when processing files', async () => {
    const testFile = new File([''], 'test.geojson', { type: 'application/geo+json' })
    const testFile2 = new File([''], 'test2.geojson', { type: 'application/geo+json' })

    initComponent({ queuedFiles: [testFile, testFile2] })

    Importer.readFiles = jest.fn()
    wrapper.vm.handleSelectedFiles([testFile, testFile2])
    wrapper.vm.prepareFiles()
    await wrapper.vm.$nextTick()
    expect(wrapper.find('filedrop-stub').exists()).toBeFalsy()
  })

  it('Shows FileDrop when processed file is invalid', async () => {
    const testFile = new File([''], 'test.exe')

    initComponent({
      queuedFiles: [testFile],
      processedFiles: [{
        filename: testFile.name,
        status: 'error',
        message: 'file of type .exe not supported.'
      }]
    })

    await wrapper.vm.$nextTick()
    expect(wrapper.find('filedrop-stub').exists()).toBeTruthy()
  })
})

describe('FileList', () => {
  let wrapper, store

  beforeEach(() => {
    const file = {
      size: 11 * 1024 * 1024 // 11mb
    }

    store = initStore({ queuedFiles: [file] })

    wrapper = shallowMount(FileList, {
      vuetify,
      store,
      propsData: {
        droppedFiles: [{ name: 'test.txt' }]
      },
      localVue
    })
  })

  it('Shows warning for files larger ' +
    'than the warning threshold', async () => {
    await wrapper.vm.$nextTick()

    expect(wrapper.find('#fileSizeWarning0').text().toLowerCase())
      .toContain('file size greater than 10 mb')
  })
})

describe('FileListProcessed', () => {
  let wrapper

  it('Displays the appropriate message', async () => {
    const fileError = {
      status: 'error',
      message: 'test error message'
    }
    const fileSuccess = {
      status: 'success',
      message: 'test error message'
    }
    const fileWarn = {
      status: 'warning',
      message: 'whatever warning'
    }
    wrapper = shallowMount(FileListProcessed, {
      vuetify,
      localVue,
      propsData: {
        files: { error: [] },
        fileLoading: []
      }
    })
    await wrapper.setProps({ files: { success: [], error: [fileError] } })

    expect(wrapper.find('#statusMessage0').text().toLowerCase())
      .toContain(fileError.message)
    expect(wrapper.find('v-alert-stub').attributes('type'))
      .toBe('error')

    await wrapper.setProps({ files: { success: [fileSuccess], error: [] } })

    expect(wrapper.find('#statusMessage0').text().toLowerCase())
      .toContain(fileSuccess.message)
    expect(wrapper.find('v-alert-stub').attributes('type'))
      .toBe('success')

    await wrapper.setProps({
      files: {
        success: [],
        error: [],
        warning: [fileWarn]
      }
    })

    expect(wrapper.find('#statusMessage0').text().toLowerCase())
      .toContain(fileWarn.message)
    expect(wrapper.find('v-alert-stub').attributes('type'))
      .toBe('warning')
  })
})
