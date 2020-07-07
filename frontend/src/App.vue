<template>
  <v-app>
    <Header :appInfo="this.app"></Header>
    <v-content>
      <v-container
        class="pa-0"
        fluid
      >
        <Toolbar/>
        <Notifications/>
        <Home/>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import Header from './components/Header'
import Toolbar from './components/Toolbar'
import Home from './components/Home'
import Notifications from './components/Notifications'
import { mapGetters, mapActions } from 'vuex'

import '@bcgov/bc-sans/css/BCSans.css'

export default {
  name: 'app',
  components: {
    Header,
    Toolbar,
    Notifications,
    Home
  },
  data: () => ({
  }),
  computed: {
    ...mapGetters(['app']),
    ...mapGetters('map', ['isMapReady'])
  },
  methods: {
    ...mapActions(['getAppInfo']),
    ...mapActions('user', ['getUserProfile']),
    ...mapGetters('user', ['defaultMapLayers'])
  },
  mounted () {
    this.getAppInfo()
    this.getUserProfile()
  },
  watch: {
    isMapReady (value) {
      if (value) {
        this.$store.dispatch('map/updateActiveMapLayers', this.defaultMapLayers() || [])
      }
    }
  }
}
</script>

<style lang="scss">
  $mdi-font-path: "~@mdi/font/fonts" !default;
  @import '~@mdi/font/scss/materialdesignicons';

  $app-font: "BCSans", "Noto Sans", Verdana, Arial, sans-serif!important;
  body {
    font-family: $app-font;
    color: #494949;

    .v-application {
      font-family: $app-font;
      .title, .headline, .body-1, .body-2,
      .display-4, .display-3, .display-2, .display-1,
      .subtitle-1, .subtitle-2, .caption, .overline {
        font-family: $app-font;
      }
    }
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
