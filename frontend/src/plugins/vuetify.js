import Vue from 'vue'
import Vuetify from 'vuetify/lib'
import 'material-design-icons-iconfont/dist/material-design-icons.css'

Vue.use(Vuetify)

export default new Vuetify({
  icons: {
    iconfont: 'mdi'
  },
  themes: {
    light: {
      primary: '#003366',
      secondary: '#F2F2F2',
      accent: '#FCBA19',
      error: '#D8292F',
      success: '#2E8540'
    },
    dark: {
      primary: '#003366'
    }
  }
})
