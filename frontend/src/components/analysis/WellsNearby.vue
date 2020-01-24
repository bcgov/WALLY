<template>
  <v-container id="wells_nearby" class="pa-0 ma-0">
    <v-row no-gutters>
      <v-col cols="12" md="4" align-self="center">
        <v-text-field
          label="Search radius (m)"
          placeholder="1000"
          :rules="[inputRules.number, inputRules.max, inputRules.required]"
          v-model="radius"
        ></v-text-field>
      </v-col>
      <v-col cols="12" offset-md="1" md="4" align-self="center" v-if="!isWellsLayerEnabled">
        <div class="caption"><a href="#" @click.prevent="enableWellsLayer">Enable groundwater wells map layer</a></div>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col>
        <v-card outlined tile>
          <v-card-text>
            <v-row>
              <v-col>
                <div class="title">Wells <span v-if="!loading">&nbsp;({{ wells.length }} in area)</span>
                </div>
              </v-col>
              <v-col class="text-right">
                  <v-btn
                    v-if="wells"
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

            <v-data-table
              :loading="loading"
              :headers="headers"
              :items="wells"
            >
              <template v-slot:item.distance="{ item }">
                <span>{{item.distance.toFixed(1)}}</span>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row no-gutters v-if="wells.length > 0" class="mt-5">
      <v-col cols="12">
        <v-card :loading="loading" outlined tile class="charts">
          <v-card-title>Insights ({{ wells.length }} wells):</v-card-title>
          <v-card-text>
            <div v-if="!loading" id="wells_charts">
              <Plotly id="boxPlotYield" :data="boxPlotYieldData.data" :layout="boxPlotYieldData.layout"></Plotly>
              <Plotly id="boxPlotFinishedDepth" :data="boxPlotFinishedDepthData.data" :layout="boxPlotFinishedDepthData.layout"></Plotly>
              <Plotly id="boxPlotSWL" :data="boxPlotSWLData.data" :layout="boxPlotSWLData.layout"></Plotly>
            </div>
          </v-card-text>
        </v-card>
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
              <p>Data on this page comes from <a href="https://apps.nrs.gov.bc.ca/gwells/" target="_blank">Groundwater Wells and Aquifers</a>.</p>
              <dl>
                <dt>Reported yield</dt>
                <dd>Estimated by the well driller during construction by conducting a well yield test. US gallons per minute.</dd>
                <dt>Static water level</dt>
                <dd>The level (from the top of the casing) to which water will naturally rise in a well without pumping, measured in feet (ft btoc).</dd>
                <dt>Top of screen</dt>
                <dd>The depth (from ground level) to the top of the uppermost reported screen segment. This figure is automatically calculated using data provided in construction reports.</dd>
                <dt>Finished well depth</dt>
                <dd>The depth at which the well was 'finished'. It can be shallower from the total well depth which is the total depth at which the well was drilled. The finished depth is represented in units of feet bgl (below ground level).</dd>
                <dt>SWL to top of screen</dt>
                <dd>The distance from the static water level to top of screen (see definition above), in feet.</dd>
                <dt>SWL to bottom of well</dt>
                <dd>The distance from the static water level to the finished well depth (see definition above), in feet.</dd>
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
