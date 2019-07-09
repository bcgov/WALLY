<template>
  <v-app>
    <Sidebar/>
    <Contextbar/>
    <WHeader></WHeader>
    <v-content>
      <v-container fluid class="pa-0 ma-0">
        <router-view/>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import WHeader from './components/Header'
import Contextbar from './components/Contextbar'
import Sidebar from './components/Sidebar'

export default {
  name: 'app',
  components: {
    Sidebar,
    WHeader,
    Contextbar
  }
}
</script>

<style lang="scss">
  body {
    font-family: ‘Noto Sans’, Verdana, Arial, sans-serif;
    color: '#494949'
  }
  a {
    color: #1A5A96;
  }
  /* noto-sans-regular - latin */
  @font-face {
    font-family: 'Noto Sans';
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
    font-style: bold;
    font-weight: 700;
    src: url('./assets/fonts/NotoSans-Bold.eot'); /* IE9 Compat Modes */
    src: local('Noto Sans'), local('NotoSans'),
    url('./assets/fonts/NotoSans-Bold.eot') format('embedded-opentype'), /* IE6-IE8 */
    url('./assets/fonts/NotoSans-Bold.woff2') format('woff2'), /* Super Modern Browsers */
    url('./assets/fonts/NotoSans-Bold.woff') format('woff'), /* Modern Browsers */
    url('./assets/fonts/NotoSans-Bold.ttf') format('truetype'), /* Safari, Android, iOS */
    url('./assets/fonts/NotoSans-Bold.svg') format('svg'); /* Legacy iOS */
  }

</style>
