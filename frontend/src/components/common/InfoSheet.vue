<template>
  <div id="info-sheet">
    <v-sheet
      elevation="5"
      v-bind:width="this.width"
      class="float-left"
    >
      <slot/>
    </v-sheet>
    <v-btn
      v-bind:style="this.closeButtonStyle"
      @click="closePanel"
      x-small
      tile
      color="white"
    ><v-icon>close</v-icon></v-btn>
  </div>
</template>
<style lang="scss">
  #info-sheet {
    position: absolute;
    z-index: 4;
    height: 100%;
    /*overflow: scroll;*/
  }
  #info-sheet > .v-sheet{
    z-index: 5;
    padding: 10px;
    height: 100%;
    overflow: scroll;
  }
  $btn-box-shadow: "0px 0px 1px -2px rgba(0,0,0,.2), 0px 0px 2px 0px rgba(0,0,0,.14), 0px 0px 5px 0px rgba(0,0,0,.12) !important";
  #info-sheet > .v-btn {
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
export default {
  name: 'InfoSheet',
  data: function () {
    return {
      closeButtonStyle: {
        left: this.width + 'px'
      }
    }
  },
  props: {
    closePanel: Function,
    display: Boolean,
    width: {
      type: Number,
      default: 800
    }
  },
  computed: {
  },
  methods: {
    handleLayerSelectionState () {
      if (!this.featureSelectionExists) {
        return this.$store.commit('setLayerSelectionActive', true)
      }
      this.$store.commit('setLayerSelectionActive', !this.layerSelectionActive)
    }
  }
}
</script>
