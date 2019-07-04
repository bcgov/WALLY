<template>
  <v-navigation-drawer
    v-model="drawer"
    app
    class="wally-sidenav"
  >
    <v-tabs
      v-model="active_tab"
      centered
      dark
      color="#38598A"
      slider-color="primary"
    >
      <v-tab v-for="tab of tabs" :key="tab.id">
        {{tab.name}}
      </v-tab>

      <v-tab-item>
        <v-list dense>
          <v-list-group
            v-for="item in items"
            :key="item.title"
            v-model="item.active"
            :prepend-icon="item.action"
            value="true"
          >
            <template v-slot:activator>
              <v-list-tile>
                <v-list-tile-content>
                  <v-list-tile-title class="wally-sidebar-category">{{ item.title }}</v-list-tile-title>
                </v-list-tile-content>
              </v-list-tile>
            </template>

            <div v-if="item.choices && item.choices.length" class="mt-3">
              <div
                v-for="choice in item.choices"
                :key="choice.id"
              >
                <p class="pl-3">
                  <label class="checkbox">{{choice.name}}
                    <input type="checkbox" @input="handleSelectLayer(choice.id)" :checked="mapLayerIsActive(choice.id)">
                    <span class="checkmark"></span>
                  </label>
                </p>
              </div>
            </div>
          </v-list-group>
        </v-list>
      </v-tab-item>

      <v-tab-item>
        <v-toolbar>
          <v-toolbar-title>Selected Points</v-toolbar-title>
        </v-toolbar>
        <div v-for="(layerGroup, groupIndex) in mapLayerSelections" :key="layerGroup.key">
          <div v-for="(value, name) in layerGroup" :key="value">
            <v-list two-line subheader>
              <v-subheader>{{mapLayerName(name)}}</v-subheader>
              <v-divider  :key="`subheader-${groupIndex}`"></v-divider>
              <template v-for="(prop, propIndex) in value">
                <v-list-tile :key="propIndex" avatar ripple>
                  <v-list-tile-content>
                    <v-list-tile-title>{{mapLayerItemTitle(name)}}</v-list-tile-title>
                    <v-list-tile-sub-title class="text--primary">{{prop.properties[mapLayerItemValue(name)]}}</v-list-tile-sub-title>
                  </v-list-tile-content>
<!--                    <v-list-tile-action>-->
<!--                      <v-list-tile-action-text>{{ item.action }}</v-list-tile-action-text>-->
<!--                      <v-icon color="grey lighten-1">star_border</v-icon>-->
<!--                    </v-list-tile-action>-->
                </v-list-tile>
                <v-divider  :key="`divider-${propIndex}`"></v-divider>
              </template>
            </v-list>
          </div>
        </div>
      </v-tab-item>

      <v-tab-item>
        <span v-html="mapLayerSingleSelection.content"></span>
      </v-tab-item>
    </v-tabs>

  </v-navigation-drawer>
</template>
<script>
import { ADD_ACTIVE_MAP_LAYER, REMOVE_ACTIVE_MAP_LAYER } from '../store/map/actions.types.js'
import { MAP_LAYERS, LAYER_PROPERTY_MAPPINGS, LAYER_PROPERTY_NAMES } from '../store/map/mapConfig'
import { mapState, mapGetters } from 'vuex'

export default {
  name: 'Sidebar',
  data () {
    return {
      active_tab: 0,
      tabs: [
        { id: 1, name: 'Mapping' },
        { id: 2, name: 'Data' },
        { id: 3, name: 'Point' }
      ],
      drawer: true,
      items: [
        {
          title: 'Layers',
          icon: 'layers',
          action: 'layers',
          choices: MAP_LAYERS
        },
        {
          title: 'Data Sources',
          icon: 'library_books',
          action: 'library_books',
          choices: this.dataLayers
        }
      ],
      mini: true
    }
  },
  computed: {
    ...mapState([
      'dataLayers']),
    ...mapGetters([
      'activeMapLayers',
      'mapLayerSelections',
      'mapLayerSingleSelection'
    ])
  },
  methods: {
    setTabById (id) {
      this.active_tab = id
    },
    handleSelectLayer (id) {
      if (this.mapLayerIsActive(id)) {
        this.$store.commit(REMOVE_ACTIVE_MAP_LAYER, id)
      } else {
        this.$store.commit(ADD_ACTIVE_MAP_LAYER, id)
      }
    },
    handleSelectListItem (item) {

    },
    mapLayerItemTitle (property) {
      return LAYER_PROPERTY_NAMES[LAYER_PROPERTY_MAPPINGS[property]]
    },
    mapLayerItemValue (property) {
      return LAYER_PROPERTY_MAPPINGS[property]
    },
    mapLayerName (layerId) {
      return this.activeMapLayers.find(e => e.wmsLayer === layerId).name
    },
    mapLayerIsActive (id) {
      if (this.activeMapLayers) {
        return this.activeMapLayers.filter(e => e.id === id).length > 0
      } else {
        return false
      }
    }
  },
  watch: {
    mapLayerSingleSelection (value) {
      if (value) {
        this.setTabById(2)
      }
    },
    mapLayerSelections (value) {
      if (value) {
        this.setTabById(1)
      }
    }
  }
}
</script>
<style lang="scss">

  .wally-sidenav {
    margin-top: 64px!important;
  }

  .wally-sidebar-category {
    font-family: ‘Noto Sans’, Verdana, Arial, sans-serif;
    font-weight: bold;
    font-size: 16px;
  }

  /* Customize the label (the container) */
  .checkbox {
    display: block;
    position: relative;
    padding-left: 25px;
    margin-bottom: 5px;
    cursor: pointer;
    Font-family: ‘Noto Sans’, Verdana, Arial, sans-serif;
    font-size: 14px;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
  }

  /* Hide the browser's default checkbox */
  .checkbox input {
    position: absolute;
    opacity: 0;
    cursor: pointer;
    height: 0;
    width: 0;
  }

  /* Create a custom checkbox */
  .checkmark {
    position: absolute;
    top: 0;
    left: 0;
    height: 16px;
    width: 16px;
    outline: 2px solid #606060;
  }

  /* When the checkbox is checked, add a blue background */
  .checkbox input:checked ~ .checkmark {
    background-color: #606060;
  }

  /* Create the checkmark/indicator (hidden when not checked) */
  .checkmark:after {
    content: "\2713";
    color: white;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    display: none;
  }

  /* Show the checkmark when checked */
  .checkbox input:checked ~ .checkmark:after {
    display: block;
  }
</style>
