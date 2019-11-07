<template>
  <v-app>
    <Header></Header>
    <v-content>
      <v-container
        class="pa-0"
        fluid
      >
        <Notifications/>
        <router-view/>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import Header from './components/common/Header'
import Toolbar from './components/toolbar/Toolbar'
import Notifications from './components/notifications/Notifications'
import '@bcgov/bc-sans/css/BCSans.css'

export default {
  name: 'app',
  components: {
    Header,
    Toolbar,
    Notifications
  },
  data: () => ({
  })
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
      .title {
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
  .container {
    height: 100%;
  }
</style>
