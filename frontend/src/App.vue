<template>
  <v-app>
    <Header></Header>
    <v-content>
      <v-container
        class="pa-0"
        fluid
      >
        <Toolbar/>
        <router-view/>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import Header from './components/Header'
import Toolbar from './components/Toolbar'
import '@bcgov/bc-sans/css/BCSans.css'

export default {
  name: 'app',
  components: {
    Header,
    Toolbar
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
</style>
