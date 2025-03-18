import { createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import * as savedAnalyses from '../../../src/store/savedAnalyses'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Saved Analyses Store', () => {
  let store
  const geometry = [
    [-123.123, 49.49],
    [-123.321, 49.94]
  ]

  beforeEach(() => {
    store = savedAnalyses.default
  })

  it('sets the saved analyses', () => {
    store.state = {
      savedAnalyses: []
    }
    store.mutations.setSavedAnalyses([{ test: 123 }])
    expect(store.getters.savedAnalyses.length).toBe(1)
  })
})
