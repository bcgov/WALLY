<template>
  <div id="legend" class="legend">
    <v-container v-for="(legendItems, layer) in legend" v-bind:key="layer">
      <h2>{{layer}}</h2>
      <div v-for="item in legendItems" v-bind:key="item.text">
        <v-icon :color="item.color">{{item.icon}}</v-icon> {{item.text}}
      </div>
    </v-container>
  </div>
</template>
<script src="./MapLegend.js"></script>
