<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="12">
        <v-expansion-panels>
          <v-expansion-panel>
            <v-expansion-panel-header>
              Instructions, Methodology, and Data Sources
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-card flat>
                <v-card-text>
                  <HydraulicConnectivityInstructions></HydraulicConnectivityInstructions>
                </v-card-text>
              </v-card>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols=12 md=6
        v-if="record && record.geometry"
      >
        <div class="pa-3 mt-3">
        Point at {{ record.geometry.coordinates.map(x => x.toFixed(6)).join(', ') }}
        </div>
      </v-col>
      <v-col class="text-right">
        <SaveAnalysisModal :geometry="record.geometry" featureType="assign-demand" />
        <v-btn @click="selectPointOfInterest" color="primary" outlined class="mt-2">Select a New Point</v-btn>
        <v-btn
          v-if="streams && streams.length"
          outlined
          :disabled="loading"
          @click="submitStreamsForExport"
          color="primary"
          class="mx-1 my-2"
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
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6" md="1">
        <span class="text-sm-right">
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn v-on:click="toggleMultiSelect" v-on="on" color="blue-grey" class="" icon>
                  <v-icon v-if="multiSelect">mdi-cancel</v-icon>
                  <v-icon v-else>mdi-pencil-box-multiple-outline</v-icon>
                </v-btn>
              </template>
              <span v-if="!multiSelect">Remove multiple streams</span>
              <span v-else>Cancel</span>
            </v-tooltip>
            <span v-show="multiSelect">
              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-btn v-on:click="removeSelected" v-on="on" color="red darken-4" class="" icon >
                    <v-icon >mdi-trash-can-outline</v-icon>
                  </v-btn>
                </template>
                <span>Remove selected</span>
              </v-tooltip>
            </span>
          </span>
      </v-col>
      <v-col cols="6" md="3">
          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
              <v-btn x-small v-show="show.removeOverlaps" v-on:click="removeOverlaps" v-on="on" color="blue-grey lighten-4" class="mb-1 mt-1">
                <span class="hidden-sm-and-down">Remove overlaps</span>
              </v-btn>
            </template>
            <span>Remove overlapping streams</span>
          </v-tooltip>
          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
              <v-btn x-small v-show="show.removeLowApportionment" v-on:click="removeStreamsWithLowApportionment(apportionmentMin)" v-on="on" color="blue-grey lighten-4" class="mb-1 mt-1">
                <span class="hidden-sm-and-down">Remove less than 10%</span>
              </v-btn>
            </template>
            <span>Remove streams that have less than 10% apportionment</span>
          </v-tooltip>
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          dense
          label="Weighting Factor"
          v-model="weightingFactor"
          :rules="[weightingFactorValidation.number, weightingFactorValidation.values, weightingFactorValidation.required]"
        >
        </v-text-field>
      </v-col>
      <v-col>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn
              v-if="app && app.config.hydraulic_connectivity_custom_stream_points"
              small v-on:click="addNewStreamPoint" v-on="on"  class="blue-grey lighten-4">
              <v-icon small>mdi-plus-circle-outline</v-icon>
              New stream point
            </v-btn>
          </template>
          <span>Add a new stream point</span>
        </v-tooltip>
      </v-col>
      <v-col>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn small v-show="show.reloadAll" v-on:click="fetchStreams" v-on="on" color="blue-grey" dark tile class="ma-2" icon>
              <v-icon >mdi-restore</v-icon>
            </v-btn>
          </template>
          <span>Reset all streams. WARNING: This will remove any custom-added stream points.</span>
        </v-tooltip>
      </v-col>
      <v-col align-self="center" v-if="!isFreshwaterAtlasStreamNetworksLayerEnabled">
        <div class="caption"><a href="#" @click.prevent="enableFreshwaterAtlasStreamNetworksLayer">Enable streams map layer</a></div>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
          <v-data-table
            :show-select="multiSelect"
            hide-default-footer
            v-model="selected"
            :loading="loading"
            :headers="headers"
            item-key="id"
            disable-pagination
            :items="streams">
            <template v-slot:item="{item}">
              <tr @mouseenter="highlight(item)" @mouseleave="highlightAll()">
                <td>{{item.gnis_name}}</td>
                <td class="text-right">{{item.length_metre.toFixed(2) | formatNumber}}</td>
                <td class="text-right">{{item.distance.toFixed(2) | formatNumber}}</td>
                <td class="text-right">{{item.apportionment.toFixed(2)}}%</td>
                <td>
                  <v-tooltip right>
                    <template v-slot:activator="{ on }">
                     <v-btn icon v-on="on" @click="deleteStream(item)">
                      <v-icon small>
                        delete
                      </v-icon>
                     </v-btn>
                    </template>
                    <span>Remove</span>
                  </v-tooltip>
                </td>
              </tr>
            </template>
          </v-data-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script src="./HydraulicConnectivity.js"></script>

<style>

</style>
