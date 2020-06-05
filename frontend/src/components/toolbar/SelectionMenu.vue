<template>
  <div>
    <v-menu offset-y>
        <template v-slot:activator="{ on }">
          <v-btn
            color="grey darken-3"
            class="ml-3 selection-menu-buttons"
            tile
            text
            v-on="on"
          >
            Selection <v-icon>keyboard_arrow_down</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item
            v-for="(item, index) in selectionOptions"
            :key="index"
            active-class="font-weight-bold"
            @click="openInfoPanelIfClosed"
            :to="item.route"
          >
            <v-list-item-icon><v-icon v-if="item.icon">{{item.icon}}</v-icon></v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>

          <!-- extra list item for resetting selections -->
          <v-list-item
            @click="resetSelections"
          >
            <v-list-item-icon><v-icon>mdi-delete-outline</v-icon></v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Reset selections</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-menu>
    <v-menu offset-y>
        <template v-slot:activator="{ on }">
          <v-btn
            color="grey darken-3"
            class="ml-3 selection-menu-buttons"
            tile
            text
            v-on="on"
          >
            Tools <v-icon>keyboard_arrow_down</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item
            v-for="(item, index) in toolOptions"
            :key="index"
            :to="item.route"
            active-class="font-weight-bold"
          >
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'SelectionMenu',
  data: () => ({
    selectionOptions: [
      {
        title: 'Place a point of interest',
        route: { name: 'point-of-interest' },
        icon: 'mdi-map-marker'
      },
      {
        title: 'Draw a polygon and search for water data',
        route: { name: 'polygon-tool' },
        icon: 'mdi-shape-polygon-plus'
      }
    ],
    toolOptions: [
      {
        title: 'Cross section plot analysis',
        route: { name: 'cross-section' }
      },
      {
        title: 'Find features upstream or downstream along a stream',
        route: { name: 'upstream-downstream' }
      },
      {
        title: 'Stream apportionment',
        route: { name: 'stream-apportionment' }
      },
      {
        title: 'Surface water availability analysis',
        route: { name: 'surface-water' }
      }

    ]
  }),
  computed: {
    ...mapGetters('map', ['map']),
    ...mapGetters(['infoPanelVisible'])
  },
  methods: {
    consoleLog () {
      global.config.debug && console.log('[wally] a')
    },
    resetSelections () {
      this.$store.dispatch('map/clearSelections')
      setTimeout(() => this.map.resize(), 0)
    },
    openInfoPanelIfClosed () {
      setTimeout(() => {
        if (!this.infoPanelVisible) {
          this.$store.commit('setInfoPanelVisibility', true)
        }
      }, 0)
    }
  }
}
</script>

<style lang="scss" scoped>
.selection-menu-buttons {
  height: 100%!important;
}
.v-list-item__content, .v-select__selection {
  text-transform: none;
}

</style>
