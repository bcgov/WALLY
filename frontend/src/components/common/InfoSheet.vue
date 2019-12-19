<template>
  <div class="info-sheet">
    <v-expand-x-transition>
      <v-sheet
        elevation="5"
        v-bind:width="this.width"
        class="float-left"
        v-show="infoPanelVisible"
      >
        <slot/>
      </v-sheet>
    </v-expand-x-transition>
    <v-slide-x-reverse-transition>
      <v-btn
        x-small
        tile
        color="white"
        @click="this.togglePanel"
        class="close"
        v-show="infoPanelVisible"
      ><v-icon>close</v-icon></v-btn>
    </v-slide-x-reverse-transition>
    <v-slide-x-transition>
      <v-btn
        v-show="!infoPanelVisible"
        @click="togglePanel()"
        large
        tile
      >
        <v-icon>mdi-arrow-expand-right</v-icon> {{this.panelName}}
      </v-btn>
    </v-slide-x-transition>
  </div>
</template>
<style lang="scss">
  $btn-box-shadow: 0px 3px 1px -2px rgba(0, 0, 0, .2), 3px 2px 2px 0px rgba(0, 0, 0, .14), 3px 1px 3px 0px rgba(0, 0, 0, .12) !important;
  #info-sheet {
    position: absolute;
    z-index: 4;
    height: calc(100vh - 120px);

    button.close {
      -webkit-box-shadow: $btn-box-shadow;
      -moz-box-shadow: $btn-box-shadow;
      box-shadow: $btn-box-shadow;
    }
  }
  #info-sheet > .v-sheet{
    z-index: 5;
    padding: 10px;
    height: 100%;
    overflow: scroll;
  }
  #info-sheet > .v-btn.close {
    z-index: 4;
    width: 20px !important;
    height: 50px;
    position: absolute;
    padding-left: 0;
    padding-right: 0;
    /* custom box shadow */
    -webkit-box-shadow: $btn-box-shadow;
    -moz-box-shadow: $btn-box-shadow;
    box-shadow: $btn-box-shadow;
  }
</style>
<script>
import { mapGetters } from 'vuex'
export default {
  name: 'InfoSheet',
  props: {
    closePanel: Function,
    display: Boolean,
    width: {
      type: Number,
      default: 800
    },
    panelName: String
  },
  data: () => {
    return {
    }
  },
  computed: {
    ...mapGetters([
      'infoPanelVisible'
    ]),
    closeButtonStyle () {
      return {
        left: this.width + 'px'
      }
    }
  },
  mounted () {
  },
  methods: {
    handleLayerSelectionState () {
      if (!this.featureSelectionExists) {
        return this.$store.commit('setLayerSelectionActive', true)
      }
      this.$store.commit('setLayerSelectionActive', !this.layerSelectionActive)
    },
    togglePanel () {
      this.$store.commit('toggleInfoPanelVisibility')
    }
  }
}
</script>
