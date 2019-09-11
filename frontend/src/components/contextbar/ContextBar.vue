<template>
  <div>
    <v-slide-x-transition>
      <v-btn  absolute dark right icon fab small color="primary" @click="toggleContextBar" v-if="!showContextBar" id="ContextButtonShow">
        <v-icon dark v-if="!showContextBar">keyboard_arrow_left</v-icon>
      </v-btn>
    </v-slide-x-transition>
    <v-slide-x-reverse-transition>
      <v-card id="contextBar" class="mx-auto" max-width="450">
        <div v-show="showContextBar" max-width="450">
          <v-card-actions>
            <v-btn small icon @click="toggleContextBar" class="minimizeContextBar" id="ContextButtonHide">
              <v-icon dark v-if="showContextBar">keyboard_arrow_right</v-icon>
            </v-btn>
          </v-card-actions>
          <span id="componentsList">
            <v-card v-for="(item, i) in contextComponents" :key="i" min-width="400" class="component">
              <v-card-title>
                <span v-if="item && item">{{item.title}}</span>
              </v-card-title>
              <v-card-text>
                <component :is="item.component" v-bind="item.data" v-bind:key="item.key"></component>
              </v-card-text>
            </v-card>
          </span>
        </div>
        <div v-if="!contextComponents.length" class="pa-3">
          <v-btn small icon @click="toggleContextBar" class="minimizeContextBar" id="ContextButtonHide">
            <v-icon dark v-if="showContextBar">keyboard_arrow_right</v-icon>
          </v-btn>
          <div class="mt-3">
            <p>Select a region using the rectangular tool or click on wells, aquifers, water licences and other features to display information.</p>
          </div>
        </div>
      </v-card>
    </v-slide-x-reverse-transition>
  </div>
</template>
<style>
#contextBar{
  position: absolute;
  right: 0;
  z-index: 3;
  height: 100%;
  overflow: scroll;
  /*min-width: 450px;*/

}
#contextBar div {
  min-width: 350px;

}
</style>
<script src="./ContextBar.js"></script>
