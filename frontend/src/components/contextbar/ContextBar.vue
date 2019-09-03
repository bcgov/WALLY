<template>
  <v-expand-transition>
      <v-card id="contextBar" class="mx-auto" max-width="450">
        <v-btn  absolute right dark icon fab small color="primary" @click="toggleContextBar" v-if="!showContextBar" id="ContextButtonShow">
          <v-icon dark v-if="!showContextBar">keyboard_arrow_left</v-icon>
        </v-btn>
          <div v-show="showContextBar">
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
      </v-card>
  </v-expand-transition>
</template>
<style>
#contextBar{
  position: absolute;
  right: 0;
  z-index: 3;
  height: 100%;
  /*min-width: 450px;*/

}
#contextBar div {
  min-width: 350px;
}
</style>
<script src="./ContextBar.js"></script>
