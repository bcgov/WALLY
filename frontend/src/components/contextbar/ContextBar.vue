<template>
  <v-expand-transition>
      <v-card id="context_bar" class="mx-auto" max-width="450">
        <v-btn absolute right dark icon fab small color="primary" @click="toggleContextBar" v-if="!showContextBar">
<!--          <v-icon dark v-if="showContextBar">keyboard_arrow_right</v-icon>-->
          <v-icon dark v-if="!showContextBar">keyboard_arrow_left</v-icon>
        </v-btn>
          <div v-show="showContextBar">
            <v-card-actions>
              <v-btn small icon @click="toggleContextBar" class="minimizeContextBar">
                <v-icon dark v-if="showContextBar">keyboard_arrow_right</v-icon>
              </v-btn>
            </v-card-actions>

            <v-card-title>Context</v-card-title>
            <span id="componentsList">
            <v-card v-for="(item, i) in contextComponents" :key="i" min-width="400" class="component">
              <v-card-title>
                <span v-if="item && item">{item.title}</span>
              </v-card-title>
              <v-card-text>
                <component :is="item.component" v-bind="item.data" v-bind:key="item.key"></component>
              </v-card-text>
            </v-card>
            </span>
          </div>
      </v-card>
  </v-expand-transition>
<!--  <v-navigation-drawer-->
<!--    v-model="drawer.open"-->
<!--    :mini-variant="drawer.mini"-->
<!--    v-bind:width="335"-->
<!--    app-->
<!--    right-->
<!--    class="wally-sidenav"-->
<!--  >-->
<!--    <v-toolbar dark color="#38598A">-->
<!--      &lt;!&ndash;      <v-toolbar-title class="white&#45;&#45;text">Data Context</v-toolbar-title>&ndash;&gt;-->
<!--      <v-spacer></v-spacer>-->
<!--      <v-btn icon @click="toggleContextBar">-->
<!--        <v-icon v-if="!drawer.mini">-->
<!--          keyboard_arrow_right-->
<!--        </v-icon>-->
<!--        <v-icon v-if="drawer.mini">-->
<!--          keyboard_arrow_left-->
<!--        </v-icon>-->
<!--      </v-btn>-->
<!--    </v-toolbar>-->
<!--    <div v-if="!drawer.mini">-->
<!--      <v-list dense>-->
<!--        <template>-->
<!--          <component v-for="item in contextComponents" :is="item.component" v-bind="item.data" v-bind:key="item.key"></component>-->
<!--        </template>-->
<!--      </v-list>-->
<!--    </div>-->
<!--  </v-navigation-drawer>-->
</template>
<style>
#context_bar{
  position: absolute;
  right: 0;
  z-index: 3;
  height: 100%;
}
</style>
<script src="./ContextBar.js"></script>
