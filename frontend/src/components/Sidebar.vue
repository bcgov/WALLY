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

<!--          <ul v-for="(value, propertyName) in mapLayerSelections">-->
<!--            <div><b>{{propertyName}}</b></div>-->
<!--            <br/>-->
<!--            <li v-for="(prop, propName) in value">-->
<!--              <div v-for="(p, v) in prop.properties">-->
<!--                <b>{{v}}:</b> {{p}}-->
<!--              </div>-->
<!--              <br/>-->
<!--            </li>-->
<!--          </ul>-->

<!--          <v-list-tile-->
<!--                  v-for="(item, i) in selectedMapObjects"-->
<!--                  :key="i"-->
<!--                  @click="handleSelectListItem(item)">-->
<!--            <v-list-tile-content class="pl-3">-->
<!--              <p class="mt-3"><a :href="item.web_uri" _target="blank">{{ JSON.stringify(item)}}</a></p>-->
<!--            </v-list-tile-content>-->
<!--          </v-list-tile>-->

        </v-list>
      </v-tab-item>

      <v-tab-item>
        <span v-html="mapLayerSingleSelectionContent"></span>
      </v-tab-item>
    </v-tabs>

  </v-navigation-drawer>
</template>
<script lang="ts">
  import { Component, Vue, Watch } from 'vue-property-decorator';
  import { mapGetters } from 'vuex';
  import { Getter } from '../store';
  import { SET_MAP_LAYER_STATE } from '../store/map/mutations.types'
  import {ADD_ACTIVE_MAP_LAYER, REMOVE_ACTIVE_MAP_LAYER} from "@/store/map/actions.types";
  import { MAP_LAYERS } from '../store/map'

  @Component({
    components: {
    },
  })
  export default class Sidebar extends Vue {
    // initial data

    get selectedMapObjects () {
      let flat: any[] | never[] = []
      Object.keys(this.mapLayerSelections).forEach((a) => {
        flat = flat.concat(this.mapLayerSelections[a])
      })
      return flat
    }

    get mapLayerSingleSelectionContent () {
      return this.$store.getters.mapLayerSingleSelection
    }

    get mapLayers () {
      return this.$store.getters.mapLayers
    }

    get dataLayers () {
      return this.$store.getters.dataLayers
    }
    get activeMapLayers () {
      return this.$store.getters.activeMapLayers
    }

    get mapLayerSelections () {
      return this.$store.getters.mapLayerSelections
    }

    get mapLayerIsActive () {
      return this.$store.getters.mapLayerIsActive
    }

    active_tab = 0
    tabs = [
      { id: 1, name: 'Mapping' },
      { id: 2, name: 'Data' },
      { id: 3, name: 'Point' }
    ]
    drawer = true;
    items = [
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
    ]
    mini = true

    setTabById(id: any) {
      this.active_tab = id
    }

    handleSelectLayer(id: any) {
      if(this.mapLayerIsActive(id)) {
        this.$store.commit(REMOVE_ACTIVE_MAP_LAYER, id)
      } else {
        this.$store.commit(ADD_ACTIVE_MAP_LAYER, id)
      }
    }

    handleSelectListItem(item: any) {

    }

    @Watch('mapLayerSingleSelectionContent')
    singleContentChanged(value: string, oldValue: string) {
      if(value) {
        this.setTabById(2)
      }
    }

    @Watch('mapLayerSelections')
    mapLayerSelectionsChanged(value: string, oldValue: string) {
      if(value) {
        this.setTabById(1)
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
