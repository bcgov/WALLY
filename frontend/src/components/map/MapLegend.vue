<template>
    <div v-if="Object.keys(legend).length > 0" id="legend" class="legend">
      <div v-for="(layer, i) in legend" v-bind:key="i">
          <h4 v-if="layer.plenty">{{layer.name}}</h4>
          <div v-for="item in layer.legendItems" v-bind:key="item.text" v-bind:class="layer.className">
            <v-icon :color="item.color" :size="item.iconSize" v-bind:style="{webkitTextStrokeWidth: item.strokeWidth, webkitTextStrokeColor: item.outlineColor}">{{item.icon}}</v-icon>
            <span v-if="layer.plenty">{{item.text}}</span>
            <span v-else>{{layer.name}}</span>
          </div>
      </div>
    </div>
</template>
<style>
  .legend {
    background-color: #fff;
    border-radius: 3px;
    bottom: 30px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.10);
    font-size: 12px;
    line-height: 20px;
    padding: 10px;
    position: absolute;
    right: 10px;
    z-index: 3;
  }

  .legend h4 {
    margin: 10px 0 0 0;
    font-weight: normal;
    font-style: italic;
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

  .legend .grouped {
    margin-left: 20px;
  }
</style>
<script src="./MapLegend.js"></script>
