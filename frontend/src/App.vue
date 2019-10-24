<template>
  <v-app>
    <Header></Header>
    <v-content>
      <v-container
        class="pa-0"
        fluid
      >
        <Toolbar/>
        <v-snackbar v-model="error" color="error" bottom right>
          <div v-if="errorMsg">{{ errorMsg }}</div>
          <div v-else>There was an error reaching the server. Please try again later.</div>
          <v-btn
            dark
            text
            timeout="6000"
            @click="error = false"
          >
            Close
          </v-btn>
        </v-snackbar>
        <router-view/>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import Header from './components/Header'
import Toolbar from './components/Toolbar'
import EventBus from './services/EventBus'

export default {
  name: 'app',
  components: {
    Header,
    Toolbar
  },
  data: () => ({
    error: false,
    errorMsg: ''
  }),
  methods: {
    clearError () {
      this.error = false
      this.errorMsg = ''
    },
    setError (msg) {
      this.clearError()
      this.error = !!msg
      if (msg && msg !== true) {
        this.errorMsg = msg
      }
    }
  },
  mounted () {
    EventBus.$on('error', this.setError)
  },
  beforeDestroy () {
    EventBus.$off('error', this.setError)
  }
}
</script>

<style lang="scss">
  $mdi-font-path: "~@mdi/font/fonts" !default;
  @import '~@mdi/font/scss/materialdesignicons';

  /* noto-sans-regular - latin */
  @font-face {
    font-family: 'Noto Sans'!important;
    font-style: normal;
    font-weight: 400;
    src: url('./assets/fonts/NotoSans-Regular.eot'); /* IE9 Compat Modes */
    src: local('Noto Sans'), local('NotoSans'),
    url('./assets/fonts/NotoSans-Regular.eot') format('embedded-opentype'), /* IE6-IE8 */
    url('./assets/fonts/NotoSans-Regular.woff2') format('woff2'), /* Super Modern Browsers */
    url('./assets/fonts/NotoSans-Regular.woff') format('woff'), /* Modern Browsers */
    url('./assets/fonts/NotoSans-Regular.ttf') format('truetype'), /* Safari, Android, iOS */
    url('./assets/fonts/NotoSans-Regular.svg') format('svg'); /* Legacy iOS */
  }

  @font-face {
    font-family: 'Noto Sans';
    font-weight: 700;
    src: url('./assets/fonts/NotoSans-Bold.eot'); /* IE9 Compat Modes */
    src: local('Noto Sans'), local('NotoSans'),
    url('./assets/fonts/NotoSans-Bold.eot') format('embedded-opentype'), /* IE6-IE8 */
    url('./assets/fonts/NotoSans-Bold.woff2') format('woff2'), /* Super Modern Browsers */
    url('./assets/fonts/NotoSans-Bold.woff') format('woff'), /* Modern Browsers */
    url('./assets/fonts/NotoSans-Bold.ttf') format('truetype'), /* Safari, Android, iOS */
    url('./assets/fonts/NotoSans-Bold.svg') format('svg'); /* Legacy iOS */
  }
  body {
    font-family: ‘Noto Sans’, Verdana, Arial, sans-serif!important;
    color: #494949;
  }
  a {
    color: #1A5A96;
  }
  .feature-content {
    user-select: auto!important;
  }
  dl > dt {
    margin-top: 1em;
    font-weight: bold;
    font-size: 1em;
  }
  dl > dd {
    font-size: 1em;
  }
</style>
