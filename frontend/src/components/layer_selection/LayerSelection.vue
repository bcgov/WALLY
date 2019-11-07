<template>
  <InfoSheet
    :closePanel="this.closePanel"
    :width="500"
  >
    <v-row>
      <v-col cols=2>

      </v-col>
      <v-col class="title" cols=6>
        Categories
      </v-col>
      <v-col cols=4 class="text-right"><v-btn @click.prevent="handleResetLayers" small color="grey lighten-2"><v-icon>refresh</v-icon>Reset all</v-btn></v-col>
    </v-row>
    <v-treeview
      selectable
      selected-color="grey darken-2"
      :value="activeMapLayers.map(layer => layer.display_data_name)"
      @input="handleSelectLayer"
      v-if="layers && categories"
      hoverable
      open-on-click
      :items="categories"
    >
      <template v-slot:label="{ item }">
        <div>
          <span>{{item.name}}</span>
          <v-dialog v-if="!item.children" width="650">
            <template v-slot:activator="{ on }">
              <v-icon class="appendRight" v-on="on">
                mdi-information-outline
              </v-icon>
            </template>
            <v-card shaped>
              <v-card-title class="headline grey lighten-3" primary-title>
                <v-icon class="mr-2">
                  mdi-information-outline
                </v-icon>
                <div style="{color:grey}">{{item.name}}</div>
              </v-card-title>
              <v-card-text class="mt-4">
                {{item.description}}
              </v-card-text>
              <v-divider></v-divider>
              <v-card-actions>
                <v-btn
                  text
                  color="primary accent-4"
                  v-bind:href=item.source_url
                  target="_blank"
                >
                  Link to Data Source
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </div>
      </template>
    </v-treeview>
<!--    <Chart :data="boxplotData.data" :layout="boxplotData.layout" :display-mode-bar="false" :key="4" class="chart"></Chart>-->
  </InfoSheet>
</template>

<script src="./LayerSelection.js"></script>

<style>
  .appendRight{
    float:right;
  }
</style>
