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
            Tools <v-icon>keyboard_arrow_down</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item
            v-for="(item, index) in toolOptions"
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
            Analysis <v-icon>keyboard_arrow_down</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item
            v-for="(item, index) in analysisOptions"
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
    defaultToolOptions: [
      {
        title: 'Place a point of interest',
        route: { name: 'point-of-interest' },
        icon: 'mdi-map-marker'
      },
      {
        title: 'Draw a polygon and search for water data',
        route: { name: 'polygon-tool' },
        icon: 'mdi-shape-polygon-plus'
      },
      {
        title: 'Measure distance and area',
        route: { name: 'measuring-tool' },
        icon: 'mdi-ruler'
      }
    ],
    analysisOptions: [
      {
        title: 'Cross section plot',
        route: { name: 'cross-section' }
      },
      {
        title: 'Upstream downstream feature search',
        route: { name: 'upstream-downstream' }
      },
      {
        title: 'Hydraulic connectivity analysis',
        route: { name: 'hydraulic-connectivity' }
      },
      {
        title: 'Surface water availability',
        route: { name: 'surface-water' }
      }

    ]
  }),
  computed: {
    toolOptions () {
      let newToolOptions = [...this.defaultToolOptions]

      let externalImport =
      {
        title: 'Upload file or data',
        route: { name: 'upload-data-layer' },
        icon: 'mdi-cloud-upload'
      }

      if (this.app && this.app.config.external_import) {
        newToolOptions.push(externalImport)
      }
      return newToolOptions
    },
    ...mapGetters('map', ['map']),
    ...mapGetters(['infoPanelVisible', 'app'])
  },
  methods: {
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
