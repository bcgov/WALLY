<template>
  <div class="home">
    <Sidebar/>
    <Map/>
  </div>
</template>

<script>
import Map from './Map'
import Sidebar from '../components/Sidebar'

export default {
  name: 'Home',
  components: {
    Map,
    Sidebar
  }
}
</script>
