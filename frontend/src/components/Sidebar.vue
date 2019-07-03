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
        <v-list dense>
          <v-list-tile>
            <v-list-tile-content class="pl-3">
              <v-list-tile-title><h2>Selected objects:</h2></v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>

<!--          <ul v-for="layerGroup in mapLayerSelections">-->
<!--            <div v-for="(value, propertyName) in layerGroup">-->
<!--              <div><b>{{propertyName}}</b></div>-->
<!--              <br/>-->
<!--              <li v-for="(prop, propName) in value">-->
<!--                <div v-for="(p, v) in prop.properties">-->
<!--                  <div v-if="v.includes('NAME')">-->
<!--                    <b>{{v}}:</b> {{p}}-->
<!--                  </div>-->
<!--                </div>-->
<!--                <br/>-->
<!--                <v-divider style="margin-bottom: 15px;"></v-divider>-->
<!--              </li>-->
<!--            </div>-->
<!--          </ul>-->
          <div v-for="layerGroup in mapLayerSelections" :key="layerGroup.key">
            <div v-for="(value, propertyName) in layerGroup" :key="value">
              <div><b>{{propertyName}}</b></div>
              <v-list-tile
                v-for="(prop, propName) in value"
                :key="propName"
                @click="handleSelectListItem(item)">
                <div v-for="(p, v) in prop.properties" :key="v">
                  <v-list-tile-content class="pl-3">
                    <p class="mt-3"><b>{{v}}:</b> {{p}}</p>
                  </v-list-tile-content>
                </div>
              </v-list-tile>
            </div>
          </div>
        </v-list>
      </v-tab-item>

      <v-tab-item>
        <span v-html="mapLayerSingleSelection.content"></span>
      </v-tab-item>
    </v-tabs>

  </v-navigation-drawer>
</template>
<script>
import { ADD_ACTIVE_MAP_LAYER, REMOVE_ACTIVE_MAP_LAYER } from '../store/map/actions.types.js'
import { MAP_LAYERS } from '../store/map/mapConfig'
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
    mapLineTitle () {

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
