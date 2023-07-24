import Vue from 'vue'
import Vuetify from 'vuetify/lib'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import colors from 'vuetify/lib/util/colors'

Vue.use(Vuetify)

const wallyColors = {
  blue: '#003366',
  light: '#F2F2F2',
  yellow: '#FCBA19',
  red: '#D8292F',
  green: '#2E8540',
  lightblue: '#1976d2'
}

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: wallyColors.lightblue,
        secondary: wallyColors.blue,
        accent: colors.shades.black,
        error: colors.red.accent3
      },
      dark: {
        primary: colors.purple,
        secondary: colors.deepPurple,
        accent: colors.amber,
        error: colors.red,
        warning: colors.amber,
        info: colors.green,
        success: colors.greenBright
      }
    }
  }
})
