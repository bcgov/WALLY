<template>
  <v-navigation-drawer
    v-model="drawer"
    v-bind:width="335"
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
        <div v-if="selectedObjects.length > 0">
          <div v-for="(layerGroup, groupIndex) in selectedObjects" :key="`objs-${layerGroup}${groupIndex}`">
            <div v-for="(value, name) in layerGroup" :key="`layerGroup-${value}${name}`">
              <v-list two-line subheader>
                <v-subheader><b>{{mapLayerName(name)}}</b></v-subheader>
                <v-divider :key="`subheader-${value}${name}`"></v-divider>
                <template v-for="(prop, propIndex) in value">
                  <v-list-tile :key="`tile-${prop}${propIndex}`" avatar ripple @click="handleSelectListItem(prop)">
                    <v-list-tile-content>
                      <v-list-tile-title>{{mapLayerItemTitle(name)}}</v-list-tile-title>
                      <v-list-tile-sub-title class="text--primary">{{prop.properties[mapLayerItemValue(name)]}}</v-list-tile-sub-title>
                    </v-list-tile-content>
  <!--                    <v-list-tile-action>-->
  <!--                      <v-list-tile-action-text>{{ item.action }}</v-list-tile-action-text>-->
  <!--                      <v-icon color="grey lighten-1">star_border</v-icon>-->
  <!--                    </v-list-tile-action>-->
                  </v-list-tile>
                  <v-divider :key="`divider-${prop}${propIndex}`"></v-divider>
                </template>
              </v-list>
            </div>
          </div>
        </div>
      </v-tab-item>

      <v-tab-item>
<!--        <span v-html="mapLayerSingleSelection.content"></span>-->
        <v-card v-if="selectedObject">
          <v-card-title class="subheading font-weight-bold">{{ mapSubheading(selectedObject.id) }}</v-card-title>

          <v-divider></v-divider>

          <v-list dense>
            <template v-for="(value, name, index) in selectedObject.properties">
              <v-list-tile :key="`tile-{$value}${index}`">
                <v-list-tile-content><b>{{ humanReadable(name) }}:</b></v-list-tile-content>
                <v-list-tile-content class="align-end">{{ value }}</v-list-tile-content>
              </v-list-tile>
              <v-divider :key="`divider-${index}`"></v-divider>
            </template>
          </v-list>
        </v-card>
      </v-tab-item>
    </v-tabs>

  </v-navigation-drawer>
</template>
<script>
import { ADD_ACTIVE_MAP_LAYER, REMOVE_ACTIVE_MAP_LAYER ,FETCH_MAP_OBJECT} from '../store/map/actions.types.js'
import { SET_SINGLE_MAP_OBJECT_SELECTION } from '../store/map/mutations.types'
import { MAP_LAYERS, LAYER_PROPERTY_MAPPINGS, LAYER_PROPERTY_NAMES } from '../store/map/mapConfig'
import { mapState, mapGetters } from 'vuex'
import { readable } from '../helpers'


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
          choices: [{
            id: 'Climate Normals 1980-2010',
            name: 'Canadian Climate Normals 1980-2010',
            uri: '',
            geojson: ''
          }]
        }
      ],
      mini: true,
      selectedObject: { content: { properties: {} } },
      selectedObjects: {},
      subHeading: ''
    }
  },
  computed: {
    ...mapGetters([
      'dataLayers',
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
      // this.$store.dispatch(FETCH_MAP_OBJECT, item.id)
      if ('LATITUDE' in item.properties && 'LONGITUDE' in item.properties) {
        item.coordinates = [item.properties['LATITUDE'], item.properties['LONGITUDE']]
      } else {
        item.coordinates = null
      }
      this.$store.commit(SET_SINGLE_MAP_OBJECT_SELECTION, item)
    },
    trimId (id) {
      return typeof (id) === 'string' ? id.substr(0, id.lastIndexOf('.')) : ''
    },
    humanReadable (val) {
      return readable(val)
    },
    mapLayerItemTitle (property) {
      return LAYER_PROPERTY_NAMES[LAYER_PROPERTY_MAPPINGS[property]]
    },
    mapLayerItemValue (property) {
      return LAYER_PROPERTY_MAPPINGS[property]
    },
    mapLayerName (layerId) {
      let layer = MAP_LAYERS.find(e => e.wmsLayer === layerId)
      if (layer) { return layer.name }
    },
    mapSubheading (id) {
      let name = this.mapLayerName(this.trimId(id))
      if (name) {
        name = name.slice(0, -1)
        return name
      }
    },
    mapLayerIsActive (id) {
      if (this.activeMapLayers) {
        let layers = this.activeMapLayers.filter(e => e.id === id)
        if (layers && layers.length) {
          return layers.length > 0
        }
      } else {
        return false
      }
    }
  },
  watch: {
    mapLayerSingleSelection (value) {
      if (value && value.properties) {
        this.selectedObject = value
        this.setTabById(2)
      } else {
        this.selectedObject = null
      }
    },
    mapLayerSelections (value) {
      if (value.length > 0) {
        this.setTabById(1)
        this.selectedObjects = value
      } else {
        this.selectedObjects = []
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
