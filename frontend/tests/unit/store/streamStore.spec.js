import { createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import * as streamStore from '../../../src/store/streamStore'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Stream Store', () => {
  var store
  beforeEach(() => {
    store = streamStore.default
  })

  it('checks store existence', () => {
    expect(store).toBeTruthy()
  })

  it('calculates upstream segments', () => {
    expect(true).toEqual(true) // placeholder
  })
})
