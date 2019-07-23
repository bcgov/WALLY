<template>
  <div class="home">
    <ContextBar/>
    <Sidebar/>
    <Map/>
  </div>
</template>

<script>
import Map from '../components/map/Map'
import Sidebar from '../components/sidebar/Sidebar.vue'
import ContextBar from '../components/contextbar/ContextBar.vue'

export default {
  name: 'Home',
  components: {
    Map,
    Sidebar,
    ContextBar
  }
}
</script>
