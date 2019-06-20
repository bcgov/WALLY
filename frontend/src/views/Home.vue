<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <p>{{msg}}</p>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component({
  components: {
  },
})
export default class Home extends Vue {
  // initial data
  private msg = 'Welcome to your Vue app!';
}
</script>
