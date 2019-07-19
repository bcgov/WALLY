<template>
  <div class="home">
    <ContextBar/>
    <Sidebar/>
    <Map/>
  </div>
</template>

<script>
import Map from '../components/map/Map'
import Sidebar from '../components/Sidebar'
import ContextBar from '../components/contextbar/ContextBar'

export default {
  name: 'Home',
  components: {
    Map,
    Sidebar,
    ContextBar
  }
}
</script>
