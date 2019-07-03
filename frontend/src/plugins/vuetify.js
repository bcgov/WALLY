import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import 'vuetify/src/stylus/app.styl';
import 'material-design-icons-iconfont/dist/material-design-icons.css'

// Helpers
import colors from 'vuetify/es5/util/colors';

Vue.use(Vuetify, {
  iconfont: 'md',
  theme: {
    primary: '#003366',
    secondary: '#F2F2F2',
    accent: '#FCBA19',
    error: '#D8292F',
    success: '#2E8540'
  }
})
