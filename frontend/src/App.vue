<template>
  <v-app>
    <w-header></w-header>
    <router-view/>
  </v-app>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import WHeader from './components/Header.vue';
@Component({
  components: {
    WHeader,
  },
})
export default class Home extends Vue {}
</script>

<style>
body {
     font-family: ‘Noto Sans’, Verdana, Arial, sans-serif;
     color: '#494949'
}
a {
  color: #1A5A96;
}
</style>