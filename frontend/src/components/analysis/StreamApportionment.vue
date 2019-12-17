<template>
  <v-container>
    <v-row>

      <v-col>
        <span class="text-sm-right">
          <span class="ma-2">
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn v-on:click="toggleMultiSelect" v-on="on" color="blue-grey" class="" icon>
                  <v-icon v-if="multiSelect">mdi-pencil-box-multiple</v-icon>
                  <v-icon v-else>mdi-pencil-box-multiple-outline</v-icon>
                </v-btn>
              </template>
              <span v-if="!multiSelect">Delete multiple rows</span>
              <span v-else>Disable MultiSelect</span>
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
          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
              <v-btn small  v-on:click="removeOverlaps" v-on="on" color="blue-grey lighten-4" class="ma-2">
                <span class="hidden-sm-and-down">Remove overlaps</span>
              </v-btn>
            </template>
            <span>Remove overlapping streams</span>
          </v-tooltip>
          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
              <v-btn small  v-on:click="removeLessThan(10)" v-on="on" color="blue-grey lighten-4" class="ma-2">
                <span class="hidden-sm-and-down">Remove less than 10%</span>
              </v-btn>
            </template>
            <span>Remove streams that have less than 10% apportionment</span>
          </v-tooltip>
          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
              <v-btn small  v-on:click="fetchStreams" v-on="on" color="blue-grey" dark tile class="ma-2" icon>
                <v-icon >mdi-restore</v-icon>
              </v-btn>
            </template>
            <span>Restore all streams</span>
          </v-tooltip>
        </span>
      </v-col>
      <v-col cols="12" offset-md="1" md="4" align-self="center" v-if="!isFreshwaterAtlasStreamNetworksLayerEnabled">
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
  </v-container>
</template>

<script src="./StreamApportionment.js"></script>

<style>

</style>
