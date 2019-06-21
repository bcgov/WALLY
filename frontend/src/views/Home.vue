<template>
  <div class="home">
    <Map2/>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Map from './Map.vue'
import Map2 from './Map2.vue'

@Component({
  components: {
    Map,
    Map2
  },
})
export default class Home extends Vue {
  // initial data
  private msg = 'Welcome to Wally!';
}
</script>
