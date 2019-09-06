import { mount, shallowMount, createLocalVue } from '@vue/test-utils'
import ContextBar from '../../src/components/contextbar/ContextBar.vue'
import Vuex from 'vuex'
import Vuetify from 'vuetify'
import Vue from 'vue'

const localVue = createLocalVue()
localVue.use(Vuex)
// localVue with Vuetify shows console warnings so we'll use Vue instead
// https://github.com/vuetifyjs/vuetify/issues/4964
// localVue.use(Vuetify)
Vue.use(Vuetify)

describe('Context Bar Tests', () => {
  let wrapper
  let store
  let getters

  beforeEach(() => {
    getters = {
      displayTemplates: () => []
    }
    store = new Vuex.Store({ getters })
    wrapper = mount(ContextBar, {
      store,
      localVue
    })
  })

  it('Button Toggles', () => {
    expect(wrapper.vm.showContextBar).toBe(false)
    wrapper.find('#ContextButtonShow').trigger('click')

    expect(wrapper.vm.showContextBar).toBe(true)
    wrapper.find('#ContextButtonHide').trigger('click')
    expect(wrapper.vm.showContextBar).toBe(false)
  })

  it('Opens the context bar', () => {
    expect(wrapper.find('#ContextButtonHide').isVisible()).toBe(false)
    wrapper.vm.openContextBar()
    expect(wrapper.find('#ContextButtonHide').isVisible()).toBe(true)
    expect(wrapper.vm.showContextBar).toBe(true)
  })
})

describe('Component builder', () => {
  let componentList = [
    {
      id: 1,
      type: 'links',
      title: 'Gov.bc.ca',
      links: ['http://www.gov.bc.ca'],
      description: 'Government of BC'
    },
    {
      id: 2,
      type: 'links',
      title: 'Gov.bc.ca',
      links: ['http://www.gov.bc.ca'],
      description: 'Government of BC'
    }
  ]
  let store
  let getters
  let wrapper
  let container, components
  beforeEach(() => {
    getters = {
      displayTemplates: () => []
    }
    store = new Vuex.Store({ getters })
    wrapper = mount(ContextBar, {
      store,
      localVue
    })

    container = wrapper.find('#componentsList')
  })

  it('Empty if there are no components', () => {
    wrapper.vm.buildComponents([])
    components = container.findAll('.component')

    expect(components.length).toBe(0)
  })

  it('Builds a component', () => {
    wrapper.vm.buildComponents(componentList)
    components = container.findAll('.component')

    expect(components.length).toBeGreaterThanOrEqual(1)
  })

  it('Creates an image', () => {
    let componentImage = {
      id: 1,
      type: 'image',
      title: 'Sample Image',
      source: 'https://www2.gov.bc.ca/assets/gov/home/gov3_bc_logo.png'
    }
    wrapper.vm.buildComponents([componentImage])
    components = container.findAll('.component')
    let image = container.find('img')

    expect(components.length).toBe(1)
    expect(image.attributes('src')).toBe(componentImage.source)
  })

  it('Creates a link set', () => {
    let componentLink = componentList[0]
    wrapper.vm.buildComponents([componentLink])
    components = container.findAll('.component')
    // let links = container.find('.links')

    expect(components.length).toBe(2)
    // TODO add back in when link component gets title
    // expect(links[0].attributes('href')).toBe(componentLink.links[0])
    // expect(link.text()).toEqual(componentLink.title)
  })

  it('Creates a title', () => {
    let componentTitle = {
      id: 1,
      type: 'title',
      title: 'Sample Title'
    }
    wrapper.vm.buildComponents([componentTitle])
    components = container.findAll('.component')
    let title = container.find('h1')

    expect(components.length).toBe(1)
    expect(title.text()).toBe(componentTitle.title)
  })

  it('Creates a card', () => {
    let componentCard = {
      id: 1,
      type: 'card',
      title: 'Hatch Creek Ranch',
      description: 'Maximum licensed demand for purpose, multiple PODs, quantity at each POD unknown'
    }
    wrapper.vm.buildComponents([componentCard])
    components = container.findAll('.component')
    let title = container.find('.title')
    let description = container.find('.description')

    expect(components.length).toBe(1)
    expect(title.text()).toBe(componentCard.title)
    expect(description.text()).toBe(componentCard.description)
  })
})
