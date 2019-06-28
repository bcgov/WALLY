<template>
  <div class="home">
    <Map/>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Map from './Map.vue'
import SuperMap from './SuperMap.vue'

@Component({
  components: {
    Map,
    SuperMap
  },
})
export default class Home extends Vue {
  // initial data
  private msg = 'Welcome to Wally!';
}
</script>
