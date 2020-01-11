<template>
  <v-container>
    <v-row>
      <v-col cols="1">
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
      <v-col>
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
      <v-col cols="3">
        <v-text-field
          dense
          label="Weighting Factor"
          v-model="weightingFactor"
          :rules="[weightingFactorValidation.number, weightingFactorValidation.max, weightingFactorValidation.required]"
        />
      </v-col>
      <v-col>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn small v-show="show.reloadAll" v-on:click="fetchStreams" v-on="on" color="blue-grey" dark tile class="ma-2" icon>
              <v-icon >mdi-restore</v-icon>
            </v-btn>
          </template>
          <span>Restore all streams</span>
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
            v-on:click:row="highlight"
            v-model="selected"
            :loading="loading"
            :headers="headers"
            item-key="ogc_fid"
            :items="streams">
            <template v-slot:item.length_metre="{ item }">
              <span>{{item.length_metre.toFixed(2)}}</span>
            </template>
            <template v-slot:item.distance="{ item }">
              <span>{{item.distance.toFixed(2)}}</span>
            </template>
            <template v-slot:item.apportionment="{ item }">
              <span>{{item.apportionment.toFixed(2)}}%</span>
            </template>
            <template v-slot:item.action="{ item }">
              <v-icon
                small
                @click="deleteStream(item)"
              >
                delete
              </v-icon>
            </template>
          </v-data-table>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col>
        <v-expansion-panels class="mt-5 elevation-0" multiple>
          <v-expansion-panel class="elevation-0">
            <v-expansion-panel-header disable-icon-rotate class="grey--text text--darken-4 subtitle-1">
              Where does this information come from?
              <template v-slot:actions>
                <v-icon color="primary">mdi-help-circle-outline</v-icon>
              </template>

            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <p>Data on this page comes from <a href="https://catalogue.data.gov.bc.ca/dataset/freshwater-atlas-stream-network" target="_blank">Freshwater Atlas Stream Network</a>.</p>
              <p>
                Computations used are from the <a href="https://www2.gov.bc.ca/gov/content/environment/air-land-water/water/water-science-data/water-science-series" target="_blank">Water Science Series</a>
                publication WSS 2016-01 (<a href="https://a100.gov.bc.ca/pub/acat/public/viewReport.do?reportId=50832" target="_blank">Determining the Likelihood of Hydraulic Connection - Guidance for Determining the Effect of Diversion of Groundwater on Specific Streams</a>)
              </p>
              <p></p>
              <dl>
                <dt>Distance</dt>
                <dd>Computed distance of the closest point of the stream to the selected point of interest</dd>
                <dt>Apportionment</dt>
                <dd>Apportion demand from diversion of groundwater on streams</dd>

              </dl>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
  </v-container>
</template>

<script src="./StreamApportionment.js"></script>

<style>

</style>
