<template>
  <div>
    <v-row>
      <v-col>
        <v-tabs>
          <v-tabs-slider></v-tabs-slider>
          <v-tab>2D Cross Section</v-tab>
          <v-tab>3D Surface Section</v-tab>
          <v-tab-item>
            <v-row>
              <v-btn small v-on:click="resetMarkerLabels" color="blue-grey lighten-4" class="ml-5 mb-1 mt-5 mr-5">
                <span class="hidden-sm-and-down"><v-icon color="secondary" class="mr-1">format_clear</v-icon>Reset Labels</span>
              </v-btn>
              <v-btn small v-on:click="downloadPlotImage" color="blue-grey lighten-4" class="mb-1 mt-5 mr-5">
                <span class="hidden-sm-and-down"><v-icon color="secondary" class="mr-1">archive</v-icon>Download 2D Plot</span>
              </v-btn>
              <v-btn small v-on:click="downloadMapImage" color="blue-grey lighten-4" class="mb-1 mt-5">
                <span class="hidden-sm-and-down"><v-icon color="secondary" class="mr-1">archive</v-icon>Download Map</span>
              </v-btn>
            </v-row>
            <v-card flat>
              <Plotly id="2dPlot" :data="chartData" :layout="chartLayout"  :modeBarButtonsToRemove="ignoreButtons" ref="crossPlot"></Plotly>
            </v-card>
          </v-tab-item>
          <v-tab-item>
            <v-card flat>
              <Plotly id="3dPlot" :data="surfaceData" :layout="surfaceLayout" ref="surfacePlot"></Plotly>
            </v-card>
          </v-tab-item>
        </v-tabs>
      </v-col>
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
  </div>
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
  font-size: 18px;
  padding-left: 5px;
  padding-top: 2px;
}
</style>
