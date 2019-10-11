<template>
    <v-row no-gutters>
      <v-col cols=12 md=7 order=0 order-md=1><Map/></v-col>
      <v-col cols=12 md=5 order=1 order-md=0><Sidebar/></v-col>
    </v-row>
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
