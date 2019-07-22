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
      <v-toolbar-title class="white--text">Data Context</v-toolbar-title>
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
<!--        <RandomChart />-->
        <BarChart :chart-data="bar_data"></BarChart>
        <v-divider></v-divider>
        <v-card style="margin-top: 25px">
          <v-img
            src="https://cdn.vuetifyjs.com/images/cards/desert.jpg"
            aspect-ratio="2.75"
          ></v-img>

          <v-card-title primary-title>
            <div>
              <h3 class="headline mb-0">Hatch Creek Ranch</h3>
              <div>
                Maximum licensed demand for purpose, multiple PODs, quantity at each POD unknown
              </div>
            </div>
          </v-card-title>
          <v-card-actions>
            <v-btn flat color="orange">Link</v-btn>
            <v-btn flat color="orange">Explore</v-btn>
          </v-card-actions>
        </v-card>
        <v-divider style="margin-top: 25px"></v-divider>
        <CircleChart/>
      </v-container>
    </div>
  </v-navigation-drawer>
</template>

<script src="./ContextBar.js">
