import Vue from 'vue'

// Simple filter to format a number nicely
Vue.filter('formatNumber', (value) => {
  return new Intl.NumberFormat().format(value)
})
