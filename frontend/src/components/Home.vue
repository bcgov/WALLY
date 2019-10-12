<template>
  <div class="home">
    <ContextBar/>
<!--    <Sidebar/>-->
    <Map/>
  </div>
</template>

<script>
import Map from './map/Map.vue'
import Sidebar from './sidebar/Sidebar.vue'
import ContextBar from './contextbar/ContextBar.vue'

export default {
  name: 'Home',
  components: {
    Map,
    Sidebar,
    ContextBar
  }
}
</script>
