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
            @click="consoleLog"
          >
            <v-list-item-title>{{ item.title }}</v-list-item-title>
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
            @click="consoleLog"
          >
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
  </div>
</template>

<script>
export default {
  name: 'SelectionMenu',
  data: () => ({
    selectionOptions: [
      {
        title: 'Place a point of interest'
      },
      {
        title: 'Draw a polygon and search for water data'
      },
      {
        title: 'Clear selections'
      }
    ],
    toolOptions: [
      {
        title: 'Plot subsurface data along a line (cross section)'
      },
      {
        title: 'Find data upstream or downstream from a point'
      },
      {
        title: 'Assign demand at a point to nearby streams'
      }
    ]
  }),
  methods: {
    consoleLog () {
      console.log('a')
    }
  }
}
</script>

<style>
.selection-menu-buttons {
  height: 100%!important;
}
</style>
