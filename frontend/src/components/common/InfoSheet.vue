<template>
  <div>
    <v-expand-x-transition group>
      <v-sheet
        elevation="5"
        width="800"
        height="100%"
        class="float-left"
        id="info-sheet"
        v-if="this.display"
      >
        <slot/>
      </v-sheet>
    </v-expand-x-transition>
    <v-fade-transition>
    <v-btn
      @click="closePanel"
      x-small
      tile
      color="white"
      v-if="this.display"
    ><v-icon>close</v-icon></v-btn>
    </v-fade-transition>
  </div>

</template>
<style>
  #info-sheet{
    position: absolute;
    z-index: 5;
    padding: 10px;
  }
  #info-sheet + .v-btn{
    z-index: 4;
    width: 20px !important;
    height: 50px;
    position: absolute;
    left: 800px;
    padding-left: 0;
    padding-right: 0;
  }
</style>
<script>
export default {
  name: 'InfoSheet',
  data: () => ({
  }),
  props: {
    closePanel: Function,
    display: Boolean
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
