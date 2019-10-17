<template>
    <v-row no-gutters class="content-wrap">
      <v-col cols=12 md=7 order=0 order-md=1><Map/></v-col>
      <v-col cols=12 md=5 order=1 order-md=0 class="content-panel"><Sidebar/></v-col>
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
<style lang="scss">
.content-wrap {
        width: 100%;
        height: calc(100vh - 120px);
    }

.content-panel {
  overflow: auto;
        height: calc(100vh - 120px);

}
</style>
