<template>
  <div id="info-sheet" ref="infoPanel">
    <v-expand-x-transition>
      <v-sheet
        elevation="5"
        class="float-left feature-info-sheet"
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
      >
        <v-icon>close</v-icon>
      </v-btn>
    </v-slide-x-reverse-transition>
    <v-slide-x-transition>
      <v-btn
        v-show="!infoPanelVisible"
        @click="togglePanel()"
        large
        tile
      >
        <v-icon>mdi-arrow-expand-right</v-icon>
        {{this.panelName}}
      </v-btn>
    </v-slide-x-transition>
    <div class="draggableBorder" v-show="infoPanelVisible"></div>
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

  #info-sheet > .v-sheet {
    z-index: 5;
    padding: 10px;
    height: 100%;
    overflow: scroll;
    width: 50vw;
  }

  @media screen and (min-width: 1900px) {
    #info-sheet > .v-sheet {
      width: 40vw;
    }
  }

  #info-sheet > .v-btn.close {
    z-index: 4;
    width: 20px !important;
    height: 50px;
    position: absolute;
    padding-left: 0;
    padding-right: 0;
  }

  .draggableBorder {
    width: 6px;
    height: 100%;
    background-color: #003366;
    opacity: 0.5;
    float: left;
    cursor: ew-resize;
    transition: opacity 0.2s ease-in-out;

    &:hover {
      opacity: 1;
    }
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
  data () {
    return {
      minPanelWidth: 300,
      panelWidth: this.width
    }
  },
  computed: {
    ...mapGetters([
      'infoPanelVisible'
    ])
  },
  mounted () {
    this.setEvents()
    this.panelWidth = this.width
  },
  updated () {
    this.panelWidth = this.width
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
    },
    setEvents () {
      const minSize = this.minPanelWidth
      const infoPanelBorder = this.$el.querySelector('.draggableBorder')
      const infoPanel = this.$el.querySelector('#info-sheet .v-sheet')

      let resize = (e) => {
        const windowWidth = document.body.scrollWidth
        const maxSize = (windowWidth / 3) * 2 // 2/3 of window width

        infoPanel.style.width = (e.clientX > minSize && e.clientX < maxSize) && e.clientX + 'px'
      }

      infoPanelBorder.addEventListener(
        'mousedown',
        () => {
          document.addEventListener('mousemove', resize, false)
        },
        false
      )

      document.addEventListener(
        'mouseup',
        () => {
          document.removeEventListener('mousemove', resize, false)
        },
        false
      )
    }
  }
}
</script>
