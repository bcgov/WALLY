<template>
  <v-sheet
    class="mt-0 px-5 fill-height"
  >
      <LayerSelection v-if="displayLayerSelection"/>
      <SingleSelectedFeature v-else-if="dataMartFeatureInfo && dataMartFeatureInfo.display_data_name"/>
      <MultipleSelectedFeatures v-else-if="dataMartFeatures && dataMartFeatures.length"/>

      <!-- nothing to display -->
      <v-card class="mt-5" v-else>
        <v-card-text>
          <!-- display a loading message if features are loading. -->
          <div v-if="loadingFeature || loadingMultipleFeatures">
            <v-progress-linear
              indeterminate
              color="primary"
              class="mb-5"
            ></v-progress-linear>
            <template v-for="n in 10">
              <v-skeleton-loader type="list-item" v-bind:key="`${n}-item`"/><v-divider v-bind:key="`${n}-divider`"/>
            </template>
          </div>
          <p v-else class="grey--text text--darken-4">Select a region using the rectangular tool or click on wells, aquifers, water licences and other features to display information.</p>
        </v-card-text>
      </v-card>
  </v-sheet>
</template>

<script src="./Sidebar.js"></script>

<style lang="scss">
  .wally-sidebar-category {
    font-weight: bold!important;
    font-size: 16px!important;
  }

  /* Customize the label (the container) */
  .checkbox {
    display: block;
    position: relative;
    padding-left: 25px;
    margin-bottom: 5px;
    cursor: pointer;
    font-size: 14px;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
  }
</style>
