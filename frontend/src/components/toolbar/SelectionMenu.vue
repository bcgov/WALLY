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
            @click="toggleInfoPanelIfClosed"
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
            @click="toggleInfoPanelIfClosed"
          >
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import EventBus from '../../services/EventBus'
export default {
  name: 'SelectionMenu',
  data: () => ({
    selectionOptions: [
      {
        title: 'Place a point of interest',
        route: { name: 'place-poi' },
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
        title: 'Plot cross section',
        route: { name: 'cross-section' }
      },
      {
        title: 'Find data upstream or downstream along a stream',
        route: { name: 'upstream-downstream' }
      },
      {
        title: 'Assign demand at a point to nearby streams',
        route: { name: 'stream-apportionment' }
      }
    ]
  }),
  computed: {
    ...mapGetters('map', ['map']),
    ...mapGetters(['infoPanelVisible'])
  },
  methods: {
    consoleLog () {
      console.log('a')
    },
    resetSelections () {
      EventBus.$emit('draw:reset', null)
      EventBus.$emit('highlight:clear')
      this.$store.commit('resetDataMartFeatureInfo')
      this.$store.commit('clearDataMartFeatures')
      this.$store.commit('clearDisplayTemplates')
      this.$store.commit('toggleInfoPanelVisibility', false)

      setTimeout(() => this.map.resize(), 0)
    },
    toggleInfoPanelIfClosed () {
      setTimeout(() => {
        if (!this.infoPanelVisible) {
          this.$store.commit('toggleInfoPanelVisibility', true)
        }
      }, 0)
    }
  }
}
</script>

<style>
.selection-menu-buttons {
  height: 100%!important;
}
</style>
