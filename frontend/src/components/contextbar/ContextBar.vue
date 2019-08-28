<template>
  <v-navigation-drawer
    v-model="drawer.open"
    :mini-variant="drawer.mini"
    v-bind:width="335"
    app
    right
    class="wally-sidenav"
  >
    <v-toolbar dark color="#38598A">
      <!--      <v-toolbar-title class="white&#45;&#45;text">Data Context</v-toolbar-title>-->
      <v-spacer></v-spacer>
      <v-btn icon @click="toggleContextBar">
        <v-icon v-if="!drawer.mini">
          keyboard_arrow_right
        </v-icon>
        <v-icon v-if="drawer.mini">
          keyboard_arrow_left
        </v-icon>
      </v-btn>
    </v-toolbar>
    <div v-if="!drawer.mini">
      <v-container>
        <component v-for="item in contextComponents" :is="item.component"  v-bind="item.data" v-bind:key="item.key"></component>
      </v-container>
    </div>
  </v-navigation-drawer>
</template>

<script src="./ContextBar.js"></script>
