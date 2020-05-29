<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="12">
        <v-expansion-panels>
          <v-expansion-panel>
            <v-expansion-panel-header>
              Instructions
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-card flat>
                <v-card-text>
                  <p>Zoom into a place of interest on the map.</p>
                  <p>Click on the "Draw a Line" button and draw a line on the map, which can be a straight line through an
                    area of wells or can be segmented to connect different wells. Double click to complete the line.
                    The buffer radius is automatically set to 200 metres and can be updated to 0 to 1000 metres after
                    your analysis is produced.</p>
                  <p>If no analysis is produced, then go to the drop down Selection menu and "Reset Selections" and try again. It also helps to have the map zoomed to a smaller area with a sufficiently large amount of detail.</p>
                  <p>When you hover over the resulting 2D and 3D graphs, a toolbar of icons will appear. To view lithology, select the box or lasso icon and then create a box or lasso over the wells in the graph that you want to see the lithology for.</p>
                  <p>The table below the graph displays the wells in your buffer radius. If you do not want a well included in your analysis, then click on the trash icon in the corresponding row and it will be removed from the graph and analysis.</p>
                  <p>Select the Excel button to download the data and information related to the wells within your cross section.</p>
                </v-card-text>
              </v-card>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6" align-self="center">
        <v-text-field
          label="Buffer radius (m)"
          placeholder="200"
          :rules="[inputRules.number, inputRules.max, inputRules.required]"
          v-model="radius"
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="6" class="text-right">
        <v-btn @click="handleRedraw" color="primary" outlined class="mt-5">Draw new line</v-btn>
      </v-col>
    </v-row>
    <v-tabs>
      <v-tabs-slider></v-tabs-slider>
      <v-tab>2D Cross Section</v-tab>
      <v-tab>3D Surface Section</v-tab>
      <v-tab-item>
        <v-row class="mb-3">
          <v-btn small v-on:click="fetchWellsAlongLine" color="blue-grey lighten-4" class="ml-5 mb-1 mt-5 mr-5">
            <span class="hidden-sm-and-down"><v-icon color="secondary" class="mr-1" size="18">refresh</v-icon>Refresh Plot</span>
          </v-btn>
          <v-btn small v-on:click="resetMarkerLabels" color="blue-grey lighten-4" class="mb-1 mt-5 mr-5">
            <span class="hidden-sm-and-down"><v-icon color="secondary" class="mr-1" size="18">format_clear</v-icon>Reset Labels</span>
          </v-btn>
          <v-btn small v-on:click="downloadMergedImage('2d')" color="blue-grey lighten-4" class="mb-1 mt-5 mr-5">
            <span class="hidden-sm-and-down"><v-icon color="secondary" class="mr-1" size="18">archive</v-icon>Download Plot</span>
          </v-btn>
        </v-row>
        <v-card-text v-if="loading" class="text-center">
          <v-progress-circular
            indeterminate
            class="my-5"
            color="grey"
          ></v-progress-circular>
        </v-card-text>
        <v-card v-else flat>
          <Plotly id="2dPlot" :data="chartData" :layout="chartLayout"  :modeBarButtonsToRemove="ignoreButtons" ref="crossPlot"></Plotly>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-row>
          <v-btn small v-on:click="fetchWellsAlongLine" color="blue-grey lighten-4" class="ml-5 mb-1 mt-5 mr-5">
            <span class="hidden-sm-and-down"><v-icon color="secondary" class="mr-1" size="18">refresh</v-icon>Refresh Plot</span>
          </v-btn>
        </v-row>
        <v-card-text v-if="loading" class="text-center">
          <v-progress-circular
            indeterminate
            class="my-5"
            color="grey"
          ></v-progress-circular>
        </v-card-text>
        <v-card v-else flat>
          <Plotly id="3dPlot" :data="surfaceData" :layout="surfaceLayout" ref="surfacePlot"></Plotly>
        </v-card>
      </v-tab-item>
    </v-tabs>
    <v-row no-gutters>
      <v-flex>
        <v-data-table
          id="cross-section-well-table"
          hide-default-footer
          v-on:click:row="highlightWell"
          v-model="selected"
          :loading="loading"
          :headers="headers"
          item-key="well_tag_number"
          :items="wells">
          <template v-slot:item.well_tag_number="{ item }">
            <span>{{item.well_tag_number}}</span>
          </template>
          <template v-slot:item.finished_well_depth="{ item }">
            <span>{{item.finished_well_depth ? item.finished_well_depth.toFixed(2) : ''}}</span>
          </template>
          <template v-slot:item.water_depth="{ item }">
            <span>{{item.water_depth ? item.water_depth.toFixed(2) : ''}}</span>
          </template>
          <template v-slot:item.action="{ item }">
            <v-icon
              small
              @click="deleteWell(item)"
            >
              delete
            </v-icon>
          </template>
        </v-data-table>
      </v-flex>
    </v-row>
    <v-row no-gutters>
      <v-col>
        <v-expansion-panels class="mt-5 elevation-0" multiple>
          <v-expansion-panel class="elevation-0">
            <v-expansion-panel-header
              disable-icon-rotate
              class="grey--text text--darken-4 subtitle-1"
            >
              Where does this information come from?
              <template v-slot:actions>
                <v-icon color="primary">mdi-help-circle-outline</v-icon>
              </template>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <p>
                Data on this page comes from
                <a
                  href="https://apps.nrs.gov.bc.ca/gwells/"
                  target="_blank"
                >Groundwater Wells and Aquifers</a> and the
                <a
                  href="https://open.canada.ca/data/en/dataset/7f245e4d-76c2-4caa-951a-45d1d2051333"
                  target="_blank"
                >Canadian Digital Elevation Model</a>.
              </p>
              <dl>
                <dt>Canadian Digital Elevation Model (CDEM)</dt>
                <dd>
                  The CDEM stems from the existing Canadian Digital Elevation Data (CDED). The latter were extracted
                  from the hypsographic andhydrographic elements of the National Topographic Data Base (NTDB) at the
                  scale of 1:50 000, the Geospatial Database (GDB), various scaled positional data acquired by the
                  provinces and territories, or remotely sensed imagery. In the CDEM data, elevations can be either
                  ground or reflective surface elevations. The CDEM data covers the Canadian Landmass.
                </dd>
                <dt>Depth to water</dt>
                <dd>
                  The depth to water, using data from <a
                  href="https://apps.nrs.gov.bc.ca/gwells/"
                  target="_blank"
                  >Groundwater Wells and Aquifers</a>.
                </dd>
                <dt>Finished well depth</dt>
                <dd>The finished well depth, as reported in the well report submitted by the well driller or pump installer (in metres).</dd>
                <dt>Well elevations</dt>
                <dd>
                  Elevations for well data (depth to water, finished well depth) are calculated by subtracting
                  the reported depth below ground level from the CDEM elevation at the location of the well.
                </dd>
              </dl>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
  </v-container>
</template>

<script src="./WellCrossSection.js"></script>

<style>
.annotationMarker {
  width: 25px;
  height: 25px;
  border-radius: 50% 50% 50% 0;
  background: #1A5A96;
  transform: rotate(-45deg);
  position: absolute;
  margin: -15px 0 0 15px;
  color: #F0FFFF;
  font-weight: bold;
  font-size: 16px;
  padding-left: 6px;
  padding-top: 2px;
}
</style>
