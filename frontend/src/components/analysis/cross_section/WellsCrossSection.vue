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
                  <CrossSectionInstructions></CrossSectionInstructions>
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
        <v-btn @click="handleRedraw" color="primary" outlined class="mt-5">Draw a new cross section</v-btn>
      </v-col>
      <v-col class="text-right">
        <v-btn
          v-if="wells && wells.length"
          outlined
          :disabled="loading"
          @click="getCrossSectionExport"
          color="primary"
        >
          Excel
          <v-icon class="ml-1" v-if="!xlsLoading">cloud_download</v-icon>
          <v-progress-circular
            v-if="xlsLoading"
            indeterminate
            size=24
            class="ml-1"
            color="primary"
          ></v-progress-circular>
        </v-btn>
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
            <span class="hidden-sm-and-down"><v-icon color="secondary" class="mr-1" size="18" v-if="!downloadImageLoading">archive</v-icon>
            <v-progress-circular
              v-if="downloadImageLoading"
              indeterminate
              size=16
              class="mr-1"
              color="secondary"
            ></v-progress-circular>
            Download Plot</span>
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
        <v-card outlined>
          <v-data-table
            id="cross-section-well-table"
            v-model="selected"
            :loading="loading"
            :headers="headers"
            :items-per-page="10"
            item-key="well_tag_number"
            :items="wells">
            <template v-slot:item="{ item }">
              <tr @mouseenter="onMouseEnterWellItem(item)">
                <td class="text-left v-data-table__divider"><a :href="`https://apps.nrs.gov.bc.ca/gwells/well/${Number(item.well_tag_number)}`" target="_blank"><span>{{item.well_tag_number}}</span></a></td>
                <td class="text-right v-data-table__divider pa-2" style="margin-left: auto; margin-right: auto;"><span>{{item.finished_well_depth ? item.finished_well_depth.toFixed(2) : ''}}</span></td>
                <td class="text-right v-data-table__divider pa-2" style="margin-left: auto; margin-right: auto;"><span>{{item.water_depth ? item.water_depth.toFixed(2) : ''}}</span></td>
                <td class="text-center v-data-table__divider pa-2"><span>{{item.aquifer && item.aquifer.aquifer_id}}</span></td>
                <td class="text-left v-data-table__divider pa-2">{{item.aquifer_lithology}}</td>
                <td class="text-leftt v-data-table__divider pa-2"><span>{{item.aquifer && item.aquifer.material_desc}}</span></td>
                <td><v-icon small @click="deleteWell(item)">delete</v-icon></td>
              </tr>
            </template>
          </v-data-table>
        </v-card>
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
                  from the hypsographic and hydrographic elements of the National Topographic Data Base (NTDB) at the
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
                  Elevations for well data (depth to water, finished well depth, etc.) are calculated by subtracting
                  the reported depth below ground level from the CDEM elevation at the location of the well.
                </dd>
                <dt>Well offset</dt>
                <dd>
                  The offset distance (in meters) and compass direction between the well head and the drawn cross section line.
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
div.plotly-notifier {
  visibility: hidden;
}
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
