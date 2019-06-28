<template>
  <div class="home">
    <Map/>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Map from './Map.vue';
import Sidebar from '../components/Sidebar.vue';
import SuperMap from './SuperMap.vue';

@Component({
  components: {
    Map,
    SuperMap,
    Sidebar
  },
})
export default class Home extends Vue {
  // initial data
  private msg = 'Welcome to Wally!';
}
</script>
