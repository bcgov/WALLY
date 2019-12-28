<template>
  <div>
    <v-menu offset-y>
        <template v-slot:activator="{ on }">
          <v-btn
            color="primary"
            class="ml-5"
            dark
            v-on="on"
          >
            Selection
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
            color="primary"
            dark
            class="ml-5"
            v-on="on"
          >
            Tools
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

</style>
