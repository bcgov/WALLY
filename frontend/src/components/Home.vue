<template>
  <div class="home d-flex">
    <PanelAdjustable/>
    <Map :style="{ width: '100vw' }"/>
    <WelcomeMessage></WelcomeMessage>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Map from '../components/map/Map.vue'
import WelcomeMessage from './WelcomeMessage'
import PanelAdjustable from './common/PanelAdjustable'

export default {
  name: 'Home',
  components: {
    PanelAdjustable,
    Map,
    WelcomeMessage
  },
  data: () => ({
    sidebarColumnDefaults: {
      cols: 12,
      md: 6,
      lg: 4,
      xl: 3
    }
  }),
  computed: {
    sidebarColumns () {
      const sidebarColumns = this.$route.meta.sidebarColumns || {}
      return Object.assign(this.sidebarColumnDefaults, sidebarColumns)
    },
    mapColumns () {
      if (this.$route.meta.hide) {
        return {
          cols: 12,
          md: 12,
          lg: 12,
          xl: 12
        }
      }
      return {
        cols: 12 - this.sidebarColumns.cols,
        md: 12 - this.sidebarColumns.md,
        lg: 12 - this.sidebarColumns.lg,
        xl: 12 - this.sidebarColumns.xl
      }
    },
    ...mapGetters('map', ['map'])
  }
}
</script>
<style lang="scss">
.home {
  height: calc(100vh - 120px);
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
