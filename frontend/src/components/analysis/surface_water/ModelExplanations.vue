<template>
  <v-row class="mx-1">
    <v-col cols="12" md="12">
      <v-expansion-panels>
        <v-expansion-panel>
          <v-expansion-panel-header>
            Model Calculations and Error
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-card flat>
              <v-card-text>
                <p>Wally uses a multi-variate linear model to calculate a number of different outputs such as mean annual runoff and monthly distribution percentages. Depending on
                where you click on the map, your point will reside within a certain hydrological zone of BC. We use different
                models for different hydrological zones.</p>

                <p>Here is an example calculation being made to calculate MAR for this Hydrological Zone {{this.defaultWatershedDetails.hydrological_zone}}.</p>
                <p>MAR = {{this.linearModelExample}}</p>

                <p>Currently we have model co-efficients for hydrological zones 25, 26, 27 which cover the south coast region.</p>
                <p>
                  Below is the co-efficients table being used for the current dropped point in Hydrological Zone {{this.defaultWatershedDetails.hydrological_zone}}.
                  The error r2, adjusted r2, and steyx values for each model are shown in the beginning of the table.
                </p>
                <p>
                  Steyx represents the standard error in the estimate of the hydrological variable (Y) as a function of the regression model (X).
                  You can find more information on what standard error is here:
                  <a href="https://en.wikipedia.org/wiki/Standard_error" target="_blank">
                    Standard Error - Wikipedia
                  </a>
                </p>

                Co-Efficients Table
                <v-data-table
                  id="model-explanations-table"
                  :headers="modelHeaders"
                  hide-default-header
                  :items="modelOutputs">
                  <template v-slot:header="{ props: { headers } }">
                    <thead>
                      <tr>
                        <th v-for="header in headers" v-bind:key="header.value">
                          <v-tooltip top>
                            <template v-slot:activator="{ on }">
                              <span v-on="on">{{header.text}}</span>
                            </template>
                            <span>{{header.tooltip}}</span>
                          </v-tooltip>
                        </th>
                      </tr>
                    </thead>
                  </template>
                  <template v-slot:item="{ item }">
                    <tr>
                      <td class="text-left v-data-table__divider"><span>{{item.output_type}}</span></td>
                      <td class="text-right v-data-table__divider pa-2" style="margin-left: auto; margin-right: auto;"><span>{{item.month}}</span></td>
                      <td class="text-center v-data-table__divider pa-2"><span>{{item.r2}}</span></td>
                      <td class="text-left v-data-table__divider pa-2">{{item.adjusted_r2}}</td>
                      <td class="text-left v-data-table__divider pa-2"><span>{{item.steyx}}</span></td>
                      <td class="text-right v-data-table__divider pa-2" style="margin-left: auto; margin-right: auto;"><span>{{item.median_elevation_co}}</span></td>
                      <td class="text-right v-data-table__divider pa-2" style="margin-left: auto; margin-right: auto;"><span>{{item.glacial_coverage_co}}</span></td>
                      <td class="text-right v-data-table__divider pa-2" style="margin-left: auto; margin-right: auto;"><span>{{item.precipitation_co}}</span></td>
                      <td class="text-right v-data-table__divider pa-2" style="margin-left: auto; margin-right: auto;"><span>{{item.potential_evapo_transpiration_co}}</span></td>
                      <td class="text-right v-data-table__divider pa-2" style="margin-left: auto; margin-right: auto;"><span>{{item.drainage_area_co}}</span></td>
                      <td class="text-right v-data-table__divider pa-2" style="margin-left: auto; margin-right: auto;"><span>{{item.solar_exposure_co}}</span></td>
                      <td class="text-right v-data-table__divider pa-2" style="margin-left: auto; margin-right: auto;"><span>{{item.average_slope_co}}</span></td>
                      <td class="text-right v-data-table__divider pa-2" style="margin-left: auto; margin-right: auto;"><span>{{item.intercept_co}}</span></td>

                    </tr>
                  </template>
                </v-data-table>

                Model Relevancy
                

              </v-card-text>
            </v-card>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-col>
  </v-row>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'ModelExplanations',
  data: () => ({
    modelHeaders: [
      { text: 'Output Type', value: 'output_type', tooltip: 'The type of value the model calculates.' },
      { text: 'Month', value: 'month', tooltip: 'Month of the year. 0 value means annual.' },
      { text: 'Med.Elev. (%/m)', value: 'median_elevation_co', tooltip: 'Median Elevation' },
      { text: 'Glc (%/%)', value: 'glacial_coverage_co', tooltip: 'Percent Glacial Coverage of the drainage area.' },
      { text: 'Precip (%/mm)', value: 'precipitation_co', tooltip: 'Annual Precipitation' },
      { text: 'PET (%/mm)', value: 'potential_evapo_transpiration_co', tooltip: 'Potential Evapo Transpiration.' },
      { text: 'DA (%/km2)', value: 'drainage_area_co', tooltip: 'Drainage area of the selected watershed.' },
      { text: 'SolExp (%/%)', value: 'solar_exposure_co', tooltip: 'Solar exposure of the area.' },
      { text: 'Slope (%/%)', value: 'average_slope_co', tooltip: 'Average slope of the drainage area.' },
      { text: 'Intercept (%)', value: 'intercept_co', tooltip: 'Model intercept co-efficient value.' },
      { text: 'R2', value: 'r2', tooltip: 'Proportion of the variance in the dependent variable that is predictable from the independent variable.' },
      { text: 'Adjusted R2', value: 'adjusted_r2', tooltip: 'R2 value that has been adjusted by number of predictors in the model.' },
      { text: 'Steyx', value: 'steyx', tooltip: 'Standard error in the estimate of the hydrological variable (Y) as a function of the regression model (X).' }
    ]
  }),
  computed: {
    ...mapGetters('surfaceWater', ['defaultWatershedDetails']),
    modelOutputs () {
      if (this.defaultWatershedDetails && this.defaultWatershedDetails.scsb2016_model &&
        !this.defaultWatershedDetails.scsb2016_model.error) {
        // console.log(this.defaultWatershedDetails.scsb2016_model)
        return this.defaultWatershedDetails.scsb2016_model.filter((x) => {
          return x.output_type !== 'MAD'
        })
      }
      return []
    },
    linearModelExample () {
      if (this.defaultWatershedDetails.scsb2016_model.error) { return }

      let mc = this.defaultWatershedDetails.scsb2016_model.find((x) => { return x.output_type === 'MAR' })
      if (mc) {
        console.log(mc.precipitation_co)
        var modelText =
          (mc.median_elevation_co !== 0 ? 'median_elevation * ' + mc.median_elevation_co + ' + ' : '') +
          (mc.glacial_coverage_co !== 0 ? 'glacial_coverage * ' + mc.glacial_coverage_co + ' + ' : '') +
          (mc.precipitation_co !== 0 ? 'precipitation * ' + mc.precipitation_co + ' + ' : '') +
          (mc.potential_evapo_transpiration_co !== 0 ? 'potential_evapo_transpiration * ' + mc.potential_evapo_transpiration_co + ' + ' : '') +
          (mc.drainage_area_co !== 0 ? 'drainage_area * ' + mc.drainage_area_co + ' + ' : '') +
          (mc.solar_exposure_co !== 0 ? 'solar_exposure * ' + mc.solar_exposure_co + ' + ' : '') +
          (mc.average_slope_co !== 0 ? 'average_slope * ' + mc.average_slope_co + ' + ' : '') +
          mc.intercept_co
        return modelText
      }
      return ''
    }
  }
}
</script>

<style>
.header-column {
  visibility: hidden;
}
</style>
