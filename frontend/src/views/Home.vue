<template>
  <div class="home">
    <Map/>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Map from './Map.vue';

@Component({
  components: {
    Map,
  },
})
export default class Home extends Vue {
  // initial data
  private msg = 'Welcome to Wally!';
}
</script>
