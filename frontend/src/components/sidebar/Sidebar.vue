<template>
  <v-navigation-drawer
    v-model="drawer"
    v-bind:width="435"
    app
    class="wally-sidenav"
  >
    <v-tabs
      v-model="active_tab"
      centered
      color="#38598A"
      slider-color="primary"
    >
      <v-tab v-for="tab of tabs" :key="tab.id">
        {{tab.name}}
      </v-tab>

      <v-tab-item>
        <v-list dense>
          <v-list-group
            v-for="item in items"
            :key="item.title"
            v-model="item.active"
            :prepend-icon="item.action"
          >
            <template v-slot:activator>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title class="wally-sidebar-category">{{ item.title }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </template>

            <div v-if="item.choices != null && item.choices.length" class="mt-3">
              <div
                v-for="choice in item.choices"
                :key="choice.display_data_name"
              >
                <p class="pl-3">
                  <label class="checkbox grey--text text--darken-4">{{choice.display_name}}
                    <input type="checkbox" @input="handleSelectLayer(choice.display_data_name, (choice.url !== '' ? 'api' : 'wms'), choice.url)" :checked="isMapLayerActive(choice.display_data_name)">
                    <span class="checkmark"></span>
                  </label>
                </p>
              </div>
            </div>
          </v-list-group>
        </v-list>
      </v-tab-item>

      <v-tab-item>
        <v-card class="mx-auto elevation-0">
          <v-list>
            <v-subheader>Selected points</v-subheader>
            <div v-for="(dataMartFeature, index) in dataMartFeatures" :key="`objs-${index}`">
              <v-list-group v-for="(value, name, j) in dataMartFeature" :key="`layerGroup-${value}${name}`" :value="~j">
                <template v-slot:activator>
                  <v-list-item-content>
                    <v-list-item-title>{{getMapLayer(name).display_name}}</v-list-item-title>
                  </v-list-item-content>
                </template>
                <v-list-item>
                  <v-list-item-content>
                      <v-data-table
                        :headers="[{ text: getMapLayer(name).label_column, value: 'col1' }]"
                        :items="value.map((x,i) => ({col1: x.properties[getMapLayer(name).label_column], id: i}))"
                        :items-per-page="10"
                        @click:row="(r) => handleFeatureItemClick(value[r.id])"
                      ></v-data-table>
                  </v-list-item-content>
                </v-list-item>
              </v-list-group>
            </div>
          </v-list>
        </v-card>
      </v-tab-item>

      <v-tab-item>

        <!-- custom components for features with visualizations etc. -->
        <component
          v-if="dataMartFeatureInfo && Object.keys(featureComponents).includes(dataMartFeatureInfo.layer_name)"
          :is="featureComponents[dataMartFeatureInfo.layer_name]"
          :record="dataMartFeatureInfo"
        />

        <!-- fallback generic feature panel for layers that do not have a custom component. Data displayed will be from
            the "highlight_columns" field of the layer catalogue.
         -->
        <v-card v-else-if="dataMartFeatureInfo">
          <v-card-title class="subheading font-weight-bold">{{ getMapSubheading(dataMartFeatureInfo.display_data_name) }}</v-card-title>

          <v-divider></v-divider>

          <v-list dense>
            <template v-for="(value, name, index) in dataMartFeatureInfo.properties">
              <v-list-item :key="`item-{$value}${index}`">
                <v-list-item-content><b>{{ humanReadable(name) }}:</b></v-list-item-content>
                <v-list-item-content class="align-end">{{ value }}</v-list-item-content>
              </v-list-item>
              <v-divider :key="`divider-${index}`"></v-divider>
            </template>
          </v-list>
        </v-card>
        <!-- <v-btn
          absolute
          dark
          fab
          top
          right
          small
          @click="createReportFromSelection"
          color="blue"
          style="margin-top: 28px"
        >
          <v-icon>cloud_download</v-icon>
        </v-btn> -->
      </v-tab-item>
    </v-tabs>

  </v-navigation-drawer>
</template>

<script src="./Sidebar.js"></script>

<style lang="scss">

  .wally-sidenav {
    margin-top: 64px!important;
  }

  .wally-sidebar-category {
    font-family: ‘Noto Sans’, Verdana, Arial, sans-serif!important;
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
    Font-family: ‘Noto Sans’, Verdana, Arial, sans-serif;
    font-size: 14px;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
  }

  /* Hide the browser's default checkbox */
  .checkbox input {
    position: absolute;
    opacity: 0;
    cursor: pointer;
    height: 0;
    width: 0;
  }

  /* Create a custom checkbox */
  .checkmark {
    position: absolute;
    top: 0;
    left: 0;
    height: 16px;
    width: 16px;
    outline: 2px solid #606060;
  }

  /* When the checkbox is checked, add a blue background */
  .checkbox input:checked ~ .checkmark {
    background-color: #606060;
  }

  /* Create the checkmark/indicator (hidden when not checked) */
  .checkmark:after {
    content: "\2713";
    color: white;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    display: none;
  }

  /* Show the checkmark when checked */
  .checkbox input:checked ~ .checkmark:after {
    display: block;
  }
</style>
