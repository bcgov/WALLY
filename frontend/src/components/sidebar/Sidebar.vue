<template>
  <v-sheet
    class="mt-0 px-5 fill-height"
  >
      <template v-if="layerSelectionActive">
        <v-row>
          <v-col cols=2>
            <v-btn
              fab
              class="elevation-1"
              small
              @click.prevent="$store.commit('setLayerSelectionActiveState', false)"
            ><v-icon>arrow_back</v-icon></v-btn>
          </v-col>
          <v-col class="title" cols=6>
            Categories
          </v-col>
          <v-col cols=4 class="text-right"><v-btn @click.prevent="handleResetLayers" small color="grey lighten-2"><v-icon>refresh</v-icon>Reset all</v-btn></v-col>
        </v-row>
        <v-treeview
          selectable
          v-model="selectedLayers"
          @input="handleSelectLayer"
          v-if="layers && categories"
          hoverable
          open-on-click
          :items="categories"
        >
          <template v-slot:label="{ item }">
            <v-hover v-slot:default="{ hover }">
              <div>
                <span>{{item.name}}</span>
                <v-icon v-if="hover" class="appendRight">info</v-icon>
              </div>
            </v-hover>
          </template>
        </v-treeview>
      </template>

      <template v-else-if="dataMartFeatureInfo && dataMartFeatureInfo.display_data_name">
        <!-- <v-sheet class="mt-3">
            <v-row align="center">
              <v-col cols=2 class="fill-height">Viewing:</v-col>
              <v-col cols=6>
                <v-select
                  outlined
                  style="margin-bottom: -1.5rem;"
                  :items="singleSelectionFeatures.map((f) => {
                    return {
                      value: f.id,
                      text: `${f.layer.id} ${f.id}`
                    }
                  })"
                ></v-select>
              </v-col>
            </v-row>
        </v-sheet> -->

        <v-row>
          <v-col cols=2>
            <v-btn
              fab
              class="elevation-1"
              small
              @click.prevent="handleCloseSingleFeature"
            ><v-icon>arrow_back</v-icon></v-btn>
          </v-col>
        </v-row>

        <!-- custom components for features with visualizations etc. -->
        <component
          v-if="dataMartFeatureInfo && Object.keys(featureComponents).includes(dataMartFeatureInfo.display_data_name)"
          :is="featureComponents[dataMartFeatureInfo.display_data_name]"
          :record="dataMartFeatureInfo"
        />

        <!-- fallback generic feature panel for layers that do not have a custom component. Data displayed will be from
            the "highlight_columns" field of the layer catalogue.
         -->
        <v-card v-else>
          <v-card-title class="subheading font-weight-bold">{{ humanReadable(dataMartFeatureInfo.display_data_name) }}</v-card-title>

          <v-divider></v-divider>

          <div v-if="featureError != ''" class="mx-3 mt-5">
            <v-alert
              border="right"
              colored-border
              type="warning"
              elevation="2"
            >
              {{featureError}}
            </v-alert>
          </div>

          <div v-if="loadingFeature">
            <template v-for="n in 10">
              <v-skeleton-loader type="list-item" v-bind:key="`${n}-item`"/><v-divider v-bind:key="`${n}-divider`"/>
            </template>
          </div>

          <v-list v-if="!loadingFeature">
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
      </template>

      <template v-else-if="dataMartFeatures && dataMartFeatures.length">
        <v-card class="elevation-0">
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
            <div class="title">Selected points
            </div>
          <v-list class="mt-5">
            <div v-for="(dataMartFeature, index) in selectedFeaturesList" :key="`objs-${index}`">

              <!--
              Using value=0 in v-list-group defaults the collapsable list item to "closed".
              In this case, keep the list items collapsed unless there is only one to display.
               -->
              <v-list-group v-for="(value, name) in dataMartFeature" :key="`layerGroup-${value}${name}`" :value="dataMartFeature.length > 1 ? 0 : 1">
                <template v-slot:activator>
                  <v-list-item-content>
                    <v-list-item-title>{{getMapLayer(name).display_name}} ({{value.length}})</v-list-item-title>
                  </v-list-item-content>
                </template>
                  <v-list-item>
                    <v-list-item-content>
                        <v-data-table
                          dense
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
      </template>

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

  .appendRight{
    float:right;
  }
</style>
