<template>
  <v-navigation-drawer
    v-model="drawer"
    app
    primary
    class="wally-sidenav"
  >

    <v-tabs
      v-model="tabs"
      centered
      dark
      color="#38598A"
      slider-color="primary"
    >
      <v-tab>
        Mapping
        
      </v-tab>
      <v-tab>
        Data
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

          <v-list-tile
            v-for="choice in item.choices"
            :key="choice"
          >
            <v-list-tile-content class="pl-3">
              <label class="checkbox">{{choice}}
                <input type="checkbox">
                <span class="checkmark"></span>
              </label>
            </v-list-tile-content>
          </v-list-tile>
          </v-list-group>
        </v-list>
      </v-tab-item>
      <v-tab-item>
        <v-list dense>
          <v-list-tile>
            <v-list-tile-content class="pl-3">
              <p>Select an object to view details.</p>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-tab-item>
    </v-tabs>
    
  </v-navigation-drawer>
</template>
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
@Component({
  components: {
  },
})
export default class Sidebar extends Vue {
  // initial data
  tab = null;
  drawer = true;
  items = [
    {
      title: 'Layers',
      icon: 'layers',
      action: 'layers',
      choices: [
        'Artesian wells',
        'Cadastral',
        'Ecocat - Water related reports',
        'Groundwater licences',
        'Observation wells - active',
        'Observation wells - inactive',
        'Wells - All'
      ]
    },
    {
      title: 'Data Sources',
      icon: 'library_books',
      action: 'library_books',
      choices: [
        'Canada Climate Data',
        'Canada Precipitation Data',
      ]
    }
  ]
  mini = true
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
