<template>
  <v-container id="wells_nearby" class="">
    <v-row no-gutters>
      <v-col cols="12" md="3" align-self="center">
        <v-text-field
          label="Search radius (m)"
          placeholder="1000"
          :rules="[inputRules.number, inputRules.max, inputRules.required]"
          v-model="radius"
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="3" align-self="center">
        <v-btn v-if="!loading && wellsByAquifer !== defaultWellsByAquifer" small v-on:click="resetWells" color="blue-grey lighten-4" class="ml-5 mb-1 mr-5">
          <span class="hidden-sm-and-down"><v-icon color="secondary" class="mr-1" size="18">refresh</v-icon>Reset Wells</span>
        </v-btn>
      </v-col>
      <v-col cols="12" offset-md="1" md="3" align-self="center" v-if="!isWellsLayerEnabled">
        <div class="caption"><a href="#" @click.prevent="enableWellsLayer">Enable groundwater wells map layer</a></div>
      </v-col>
      <v-col v-else>
        <v-spacer/>
      </v-col>
      <v-col cols="12" md="3" class="text-right">
        <v-btn @click="selectPoint" color="primary" outlined class="mt-2">Draw new point</v-btn>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-card outlined tile width="100%">
        <v-card-text>
          <v-row>
            <v-col>
              <div class="title">Wells <span v-if="!loading">&nbsp;({{ this.wellCount }} in area)</span>
              </div>
            </v-col>
            <v-col class="text-right">
              <v-btn
                v-if="wellsByAquifer"
                outlined
                :disabled="loading"
                @click="exportDrawdownAsSpreadsheet"
                color="primary"
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
          <v-row v-if="loading">
            <v-progress-linear indeterminate></v-progress-linear>
          </v-row>
          <v-row>
            <!-- Wells by aquifer-->
            <v-expansion-panels
              v-for="(wells, aquifer) in wellsByAquifer" v-bind:key="aquifer"
              :value=wellsByAquiferIndexes
              tile focusable multiple>
              <v-expansion-panel class="wells-by-aquifer">
                <v-expansion-panel-header>
                  Aquifer: {{aquifer ? aquifer : 'Uncorrelated'}} ({{wells.length}} wells)
                </v-expansion-panel-header>
                <v-expansion-panel-content width="100%">
                  <v-card outlined width="1000px" class="mt-5">
                    <v-data-table
                      :loading="loading"
                      :headers="headers"
                      :items="wells"
                    >
                      <template v-slot:item="{ item }">
                        <tr @mouseenter="onMouseEnterWellItem(item)">
                          <td class="text-left v-data-table__divider pa-2"><v-icon small @click="deleteWell(aquifer, item)">delete</v-icon></td>
                          <td class="text-right v-data-table__divider pa-2"><span>{{item.distance ? item.distance.toFixed(1) : ''}}</span></td>
                          <td class="text-left v-data-table__divider pa-2"><a :href="`https://apps.nrs.gov.bc.ca/gwells/well/${Number(item.well_tag_number)}`" target="_blank"><span>{{item.well_tag_number}}</span></a></td>
                          <td class="text-right v-data-table__divider pa-2"><span>{{item.well_yield ? item.well_yield : ''}}</span></td>
                          <td class="text-right v-data-table__divider pa-2"><span>{{item.static_water_level ? item.static_water_level : ''}}</span></td>
                          <td class="text-right v-data-table__divider pa-2"><span>{{item.top_of_screen ? item.top_of_screen : ''}}</span></td>
                          <td class="text-right v-data-table__divider pa-2"><span>{{item.finished_well_depth ? item.finished_well_depth.toFixed(2) : ''}}</span></td>
                          <td class="text-right v-data-table__divider pa-2"><span>{{item.swl_to_screen ? item.swl_to_screen : ''}}</span></td>
                          <td class="text-right v-data-table__divider pa-2"><span>{{item.swl_to_bottom_of_well ? item.swl_to_bottom_of_well : ''}}</span></td>
                          <td class="text-center v-data-table__divider pa-2"><span>{{item.aquifer && item.aquifer.aquifer_id}}</span></td>
                          <td class="text-left v-data-table__divider pa-2"><span>{{item.aquifer_lithology ? item.aquifer_lithology : ''}}</span></td>
                          <td class="text-left pa-2"><span>{{item.aquifer && item.aquifer.material_desc}}</span></td>
                        </tr>
                      </template>
                    </v-data-table>
                  </v-card>
                  <!-- Boxplot Whisker graphs.
                       Aquifer 1143 contains wells that have been attempted to be correlated to an aquifer-->
                  <v-alert v-if="aquifer && Number(aquifer) === 1143" type="info" text class="alert mt-5">
                    <p>
                      Wells not correlated to an aquifer at time of interpretation due to insufficient information.
                    </p>
                  </v-alert>
                  <WellsNearbyBoxPlot :wells="wells" v-if="aquifer && Number(aquifer) !== 1143"/>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-row>
        </v-card-text>
      </v-card>
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
              <p>Data on this page comes from <a href="https://apps.nrs.gov.bc.ca/gwells/" target="_blank">Groundwater Wells and Aquifers</a>.</p>
              <dl>
                <dt>Reported yield</dt>
                <dd>Estimated by the well driller during construction by conducting a well yield test. Values are in US gallons per minute.</dd>
                <dt>Static water level</dt>
                <dd>The level (from the top of the casing) to which water will naturally rise in a well without pumping, measured in feet below top of casing (ft btoc).</dd>
                <dt>Top of screen</dt>
                <dd>The depth (from ground level) to the top of the uppermost reported screen segment. This figure is automatically calculated using data provided in construction reports.</dd>
                <dt>Finished well depth</dt>
                <dd>The depth at which the well was 'finished'. It can be shallower from the total well depth which is the total depth at which the well was drilled. The finished depth is represented in units of feet below ground level (ft bgl).</dd>
                <dt>SWL to top of screen</dt>
                <dd>The distance from the static water level to top of screen (see definition above) in feet.</dd>
                <dt>SWL to bottom of well</dt>
                <dd>The distance from the static water level to the finished well depth (see definition above) in feet.</dd>
                <dt>Aquifer Number</dt>
                <dd>A unique number assigned to an aquifer and represents the aquifer that a well has been correlated to.</dd>
                <dt>Aquifer Lithology</dt>
                <dd>Represents the type of material an aquifer consists of and is described by values of consolidated and unconsolidated.</dd>
                <dt>Aquifer Material</dt>
                <dd>Describes the broad grouping of geological material found in the aquifer.</dd>
              </dl>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
  </v-container>
</template>

<script src="./WellsNearby.js"></script>
<style lang="scss">
 #wells_nearby{
  .plot-container{
    width: 220px;
    float: left;
  }
   .v-card.charts{
     min-height: 460px
   }
 }
</style>
