import { createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import * as streamStore from '../../../src/store/streamStore'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Stream Store', () => {
    let store
    beforeEach(() => {
        store = streamStore.default
    })

    it('calculates upstream segments', () => {
        expect(true).toEqual(true) // placeholder
    })
    
})