<!--<template>-->
<!--    <v-row no-gutters class="content-wrap">-->
<!--      <v-col cols=12 md=7 order=0 order-md=1><Map/></v-col>-->
<!--      <v-col cols=12 md=5 order=1 order-md=0 class="content-panel"><Sidebar/></v-col>-->
<!--    </v-row>-->
<!--</template>-->
<template>
  <div class="home">
    <Navigation/>
    <LayerSelection/>
    <Toolbar/>
    <Map/>
  </div>
</template>
<script>
import Map from '../map/Map.vue'
import Sidebar from '../sidebar/Sidebar.vue'
import Navigation from '../navigation/Navigation.vue'
import LayerSelection from '../layer_selection/LayerSelection.vue'

export default {
  name: 'Home',
  components: {
    Map,
    Sidebar,
    Navigation,
    LayerSelection
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
