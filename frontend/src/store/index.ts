import Vue from 'vue'
import Vuex from 'vuex'
import { createDecorator } from 'vue-class-component'

import map from './map'

Vue.use(Vuex)

export function Getter (getterType: any) {
  return createDecorator((options, key) => {
    if (!options.computed) options.computed = {}
    options.computed[key] = function () {
      // @ts-ignore
      return this.$store.getters[getterType]
    }
  })
}

export default new Vuex.Store({
  modules: {
    map: map,
  }
})
