<template>
  <div class="home">
    <Sidebar></Sidebar>
    <Map></Map>
  </div>
</template>

<script>
import Map from '../components/map/Map.vue'
import Sidebar from '../components/sidebar/Sidebar.vue'

export default {
  name: 'Home',
  components: {
    Map,
    Sidebar
  }
}
</script>
<style lang="scss">
.home {
  height: calc(100vh - 64px);
}
.content-wrap {
  width: 100%;
  height: calc(100vh - 120px);
}

.content-panel {
  overflow: auto;
  height: calc(100vh - 120px);

}
/* Custom animations for router-view transitions */
.expand-x-enter, .expand-x-leave-to {
  width: 0;
}
$expand-transition: "width 1s ease-in-out, opacity 03s ease 0.5s";
.expand-x-enter-active, .expand-x-leave-active {
  -webkit-transition: $expand-transition;
  -moz-transition: $expand-transition;
  -o-transition: $expand-transition;
  transition: $expand-transition;
  transition-duration: 0.3s;
  overflow: hidden;
}
.expand-x-enter-to, .expand-x-leave { width: 100%; }
</style>
