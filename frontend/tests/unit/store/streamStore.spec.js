import { createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Stream Store', () => {
  beforeEach(() => {
  })

  it('calculates upstream segments', () => {
    expect(true).toEqual(true) // placeholder
  })
})
