<template>
  <div class="home">
    <Contextbar/>
    <Sidebar/>
    <Map/>
  </div>
</template>

<script>
import Map from './Map'
import Sidebar from '../components/Sidebar'
import Contextbar from './components/Contextbar'

export default {
  name: 'Home',
  components: {
    Map,
    Sidebar
  }
}
</script>
