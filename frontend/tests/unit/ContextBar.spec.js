import { mount, shallowMount, createLocalVue } from '@vue/test-utils'
import ContextBar from '../../src/components/contextbar/ContextBar.vue'
import Vuex from 'vuex'
import Vue from 'vue'
import Vuetify from 'vuetify'

Vue.use(Vuetify)

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Context Bar Tests', () => {
  let store
  let getters
  let wrapper

  beforeEach(() => {
    getters = {
      dataMartFeatures: () => []
    }
    store = new Vuex.Store({ getters })
    wrapper = mount(ContextBar, {
      store,
      localVue
    })
  })

  it('Toggles', () => {
    let button = wrapper.find('.v-card button.v-btn')

    button.trigger('click')
    expect(wrapper.vm.showContextBar).toBeTruthy()

    button = wrapper.find('.v-btn.minimizeContextBar')
    button.trigger('click')
    expect(wrapper.vm.showContextBar).toBeFalsy()
  })

  it('Opens the context bar', () => {
    wrapper.vm.openContextBar()
    expect(wrapper.vm.showContextBar).toBeTruthy()
  })
})
describe('Component builder', () => {
  let componentList = [
    {
      id: 1,
      type: 'link',
      title: 'Gov.bc.ca',
      url: 'http://www.gov.bc.ca',
      description: 'Government of BC'
    },
    {
      id: 2,
      type: 'link',
      title: 'Gov.bc.ca',
      url: 'http://www.gov.bc.ca',
      description: 'Government of BC'
    }
  ]

  let store
  let getters
  let wrapper
  let container
  beforeEach(() => {
    getters = {
      dataMartFeatures: () => []
    }
    store = new Vuex.Store({ getters })
    wrapper = mount(ContextBar, {
      store,
      localVue
    })

    container = wrapper.find('#componentsList')
  })

  it('Empty if there are no components', () => {
    expect(container.isEmpty())
  })

  it('Builds a component', () => {
    wrapper.setData({ contextComponents: componentList })
    expect(!container.isEmpty())
  })

  it('Builds components', () => {
    wrapper.setData({ contextComponents: componentList })
    let components = wrapper.findAll('#componentsList .component')
    expect(components.length).toBe(2)
  })

  it('Creates a link', () => {
    let componentLink = {
      id: 1,
      type: 'link',
      title: 'Gov.bc.ca',
      source: 'http://www.gov.bc.ca',
      description: 'Government of BC'
    }
    wrapper.setData({ contextComponents: componentLink })

    let a = wrapper.find('#componentsList a')
    expect(!a.isEmpty())
    expect(a.text()).toEqual('Gov.bc.ca')
    expect(a.attributes('href')).toBe(componentLink.source)
  })

  it('Creates a chart', () => {
    let componentChart = {
      id: 1,
      type: 'chart',
      data: {
        type: 'bar', // combo, line, pie, etc
        label: 'Water Quantity',
        datasets_labels: ['Water Quantity'],
        label_key: 'LICENCE_NUMBER',
        datasets_key: ['QUANTITY']
      }
    }

    wrapper.setData({ contextComponents: componentChart })

    let chart = wrapper.find('#componentsList .chart')
    expect(chart).toBeDefined()
  })

  it('Creates a card', () => {
    let componentCard = {
      id: 1,
      type: 'card',
      title: 'Sample Card',
      data: 'Card data'
    }

    wrapper.setData({ contextComponents: componentCard })

    let card = wrapper.find('#componentsList .card')
    expect(card).toBeDefined()
  })

  it('Creates an image', () => {
    let componentImage = {
      id: 1,
      type: 'image',
      title: 'Sample Image',
      source: 'https://www2.gov.bc.ca/assets/gov/home/gov3_bc_logo.png'
    }

    wrapper.setData({ contextComponents: componentImage })

    let image = wrapper.find('#componentsList img')
    expect(image).toBeDefined()
    expect(image.attributes('src')).toBe(componentImage.source)
  })
})
