import { createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import * as crossSectionStore from '../../../src/store/crossSection'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Cross Section Store', () => {
  let store
  let payload = [
    [-123.123, 49.49],
    [-123.321, 49.94]
  ]

  beforeEach(() => {
    store = crossSectionStore.default
  })

  it('gets the cross section line', () => {
    store.state = {
      sectionLine: payload
    }
    let sectionLine = store.getters.sectionLine(store.state)
    expect(sectionLine).toBe(payload)
  })

  it('sets the cross section line', () => {
    store.state = {
      sectionLine: null
    }
    store.mutations.setSectionLine(store.state, payload)
    expect(store.state.sectionLine).toBe(payload)
  })

  it('resets the cross section line', () => {
    store.state = {
      sectionLine: payload
    }
    store.mutations.resetSectionLine(store.state)
    expect(store.state.sectionLine).toBe(null)
  })
})
