<template>
  <div class="home">
    <ContextBar/>
    <Map/>
  </div>
</template>

<script>
import Map from './map/Map.vue'
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
