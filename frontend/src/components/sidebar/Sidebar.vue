<template>
  <v-navigation-drawer
    app
    v-model="drawer"
    v-bind:width="435"
    class="wally-sidenav"
    clipped
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

      <v-tab-item class="pa-5">
        <v-row>
          <v-col class="title">Categories</v-col>
          <v-col class="text-right"><v-btn @click.prevent="handleResetLayers" small color="grey lighten-2"><v-icon>refresh</v-icon>Reset all</v-btn></v-col>
        </v-row>
        <v-treeview
          selectable
          v-model="selectedLayers"
          @input="handleSelectLayer"
          v-if="layers && categories"
          :items="categories"
        ></v-treeview>
      </v-tab-item>

      <v-tab-item>
        <v-card class="mx-auto elevation-0">
          <v-card-text>
            <span class="float-right mt-3">
              <v-btn
                v-if="dataMartFeatures && dataMartFeatures.length"
                dark
                @click="createSpreadsheetFromSelection"
                color="blue"
              >
                Excel
                <v-icon class="ml-1" v-if="!spreadsheetLoading">cloud_download</v-icon>
                <v-progress-circular
                  v-if="spreadsheetLoading"
                  indeterminate
                  size=24
                  class="ml-1"
                  color="primary"
                ></v-progress-circular>
              </v-btn>
              <v-btn
                v-if="dataMartFeatures && dataMartFeatures.length"
                dark
                @click="createPdfFromSelection"
                color="blue"
                class="ml-2"
              >
                PDF
                <v-icon class="ml-1" v-if="!pdfReportLoading">picture_as_pdf</v-icon>
                <v-progress-circular
                  v-if="pdfReportLoading"
                  indeterminate
                  size=24
                  class="ml-1"
                  color="primary"
                ></v-progress-circular>
              </v-btn>
            </span>

          <v-list>
            <div class="title">Selected points
            </div>
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
                        >
                          <template v-slot:item="{ item }">
                            <v-hover v-slot:default="{ hover }" v-bind:key="`list-item-{$value}${item.id}`">
                              <v-card
                                class="px-2 py-3 mx-1 my-2"
                                :elevation="hover ? 2 : 0"
                                @mousedown="setSingleListFeature(value[item.id], name)"
                                @mouseenter="onMouseEnterListItem(value[item.id], name)"
                              >
                                <span>{{ item.col1 }}</span>
                              </v-card>
                            </v-hover>
                            <v-divider :key="`divider-${item.id}`"></v-divider>
                          </template>
                        </v-data-table>
                    </v-list-item-content>
                  </v-list-item>
              </v-list-group>
            </div>
          </v-list>
          </v-card-text>

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
          <v-card-title class="subheading font-weight-bold">{{ humanReadable(dataMartFeatureInfo.display_data_name) }}</v-card-title>

          <v-divider></v-divider>

          <v-list>
            <template v-for="(value, name, index) in getHighlightProperties(dataMartFeatureInfo)">
              <v-hover v-slot:default="{ hover }" v-bind:key="`item-{$value}${index}`">
                <v-card
                  class="pl-3 mb-2 pt-2 pb-2"
                  :elevation="hover ? 12 : 2"
                >
                  <span><b>{{ humanReadable(name) }}: </b></span>
                  <span>{{ value }}</span>
                </v-card>
              </v-hover>
              <v-divider :key="`divider-${index}`"></v-divider>
            </template>
          </v-list>
        </v-card>
      </v-tab-item>
    </v-tabs>

  </v-navigation-drawer>
</template>

<script src="./Sidebar.js"></script>

<style lang="scss">

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
