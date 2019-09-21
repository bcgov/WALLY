<template>
    <div v-if="Object.keys(legend).length > 0" id="legend" class="legend">
      <div v-for="(legendItems, layer) in legend" v-bind:key="layer">
<!--        <div v-if="legendItems.length > 1">-->
          <h2 v-if="legendItems.length > 1">{{layer}}</h2>
          <div v-for="item in legendItems" v-bind:key="item.text">
            <v-icon :color="item.color" :size="item.iconSize">{{item.icon}}</v-icon>
            <span v-if="legendItems.length > 1">{{item.text}}</span>
            <span v-else>{{layer}}</span>
          </div>
<!--        <div v-else>-->
<!--          <v-icon :color="legendItems[0].color" :size="legendItems[0].iconSize">{{legendItems[0].icon}}</v-icon>-->
<!--          {{layer}}-->
<!--        </div>-->
      </div>
    </div>
</template>
<style>
  .legend {
    background-color: #fff;
    border-radius: 3px;
    bottom: 30px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.10);
    font: 12px/20px 'Helvetica Neue', Arial, Helvetica, sans-serif;
    padding: 10px;
    position: absolute;
    right: 10px;
    z-index: 3;
  }

  .legend h4 {
    margin: 0 0 10px;
  }

  .legend div span {
    border-radius: 50%;
    display: inline-block;
    height: 10px;
    margin-right: 5px;
    margin-left: 5px;
  }

  .legend .v-icon {
    width: 20px;
  }
</style>
<script src="./MapLegend.js"></script>
