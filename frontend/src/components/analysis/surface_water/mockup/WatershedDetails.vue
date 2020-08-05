<template>
  <v-card flat>
    <v-card-text>
      <v-select
        :items="watershedSelect"
        :menu-props="{ maxHeight: '400' }"
        label="Watershed"
        item-text="label"
        item-value="value"
        hint="Select from available watersheds at this location"
      ></v-select>
      <v-row>
        <v-alert tile color="" dense class="ma-3" width="100%" text>
            Model output based on South Coast Stewardship Baseline (Sentlinger, 2016).
        </v-alert>
        <v-expansion-panels  class="pl-3 pr-3 elevation-0"  tile  >
          <v-expansion-panel>
            <v-expansion-panel-header class="" >
                Model Calculations and Error
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <p>Wally uses a multi-variate linear model to calculate a number of different outputs such as mean annual runoff and monthly distribution percentages. Depending on
                where you click on the map, your point will reside within a certain hydrological zone of BC. We use different
                models for different hydrological zones.</p>

              <p>Here is an example calculation being made to calculate MAR for this Hydrological Zone <v-icon>text_fields</v-icon>.</p>
              <p>MAR = <v-icon>text_fields</v-icon></p>

              <p>Currently we have model co-efficients for hydrological zones 25, 26, 27 which cover the south coast region.</p>
              <p>
                Below is the co-efficients table being used for the current dropped point in Hydrological Zone <v-icon>text_fields</v-icon>.
                The error r2, adjusted r2, and steyx values for each model are shown in the far right of the table.
              </p>

              Co-Efficients Table
              <v-divider></v-divider>
              <v-icon x-large>table_chart</v-icon>
            </v-expansion-panel-content>
          </v-expansion-panel>

        </v-expansion-panels>
      </v-row>
      <v-row>
        <v-col>
          <v-card flat outlined tile>
            <v-card-title>
              Drainage area
              <v-icon small class="ml-1">mdi-information-outline</v-icon>
            </v-card-title>
            <v-card-text class="info-blue">
              <!--                    <v-icon class="ml-1">functions</v-icon>-->
<!--              <v-icon class="ml-1">text_fields</v-icon>-->
<!--              <v-icon class="ml-1">mdi-format-superscript</v-icon>-->
              0000
              <strong>km²</strong>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-card flat >
          <v-card-title>
            Mean Annual Discharge
            <v-icon small class="ml-1">mdi-information-outline</v-icon>
          </v-card-title>
          <v-card-text class="info-blue">
<!--            <v-icon class="ml-1">text_fields</v-icon>-->
            0000
            <strong>m³/s
            </strong>
          </v-card-text>
        </v-card>
        <v-divider vertical></v-divider>
        <v-card flat >
          <v-card-title>
            Total Annual Quantity
            <v-icon small class="ml-1">mdi-information-outline</v-icon>

          </v-card-title>
          <v-card-text class="info-blue">
<!--            <v-icon class="ml-1">text_fields</v-icon>-->
            000
            <strong>m³
            </strong>
          </v-card-text>
        </v-card>
      </v-row>
      <v-divider></v-divider>
      <v-row>
        <v-card flat >
          <v-card-title>
            Mean Annual Runoff
            <v-icon small class="ml-1">mdi-information-outline</v-icon>
          </v-card-title>
          <v-card-text class="info-blue">
<!--            <v-icon class="ml-1">text_fields</v-icon>-->
            0000
            <strong>
              l/s/km²
            </strong>
          </v-card-text>
        </v-card>
        <v-divider vertical></v-divider>
        <v-card flat >
          <v-card-title>
            Low7Q2
            <v-icon small class="ml-1">mdi-information-outline</v-icon>

          </v-card-title>
          <v-card-text class="info-blue">
            000
<!--            <v-icon class="ml-1">text_fields</v-icon>-->
            <strong>m³
            </strong>
          </v-card-text>
        </v-card>
        <v-divider vertical></v-divider>

        <v-card flat >
          <v-card-title>
            Dry7Q10
            <v-icon small class="ml-1">mdi-information-outline</v-icon>
          </v-card-title>
          <v-card-text class="info-blue">
            000
<!--            <v-icon class="ml-1">text_fields</v-icon>-->
            <strong>
              m³/s
            </strong>
          </v-card-text>
        </v-card>
      </v-row>
      <v-divider></v-divider>
      <v-row>
        <v-card flat >
          <v-card-title>
            Annual Precipitation
            <v-icon small class="ml-1">mdi-information-outline</v-icon>
          </v-card-title>
          <v-card-text class="info-blue">
<!--            <v-icon class="ml-1">text_fields</v-icon>-->
            000
            <strong>mm</strong>
          </v-card-text>
        </v-card>
        <v-divider vertical></v-divider>
        <v-card flat >
          <v-card-title>
            Glacial Coverage
            <v-icon small class="ml-1">mdi-information-outline</v-icon>
          </v-card-title>
          <v-card-text class="info-blue">
<!--            <v-icon class="ml-1">text_fields</v-icon>-->
            000
          </v-card-text>
        </v-card>
        <v-divider vertical></v-divider>

        <v-card flat >
          <v-card-title>
            Median Elevation
            <v-icon small class="ml-1">mdi-information-outline</v-icon>
          </v-card-title>
          <v-card-text class="info-blue">
<!--            <v-icon class="ml-1">text_fields</v-icon>-->
            000
            <strong>mASL</strong>
          </v-card-text>
        </v-card>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'WatershedDetails',
  components: {
    // ModelExplanations

  },
  data: () => ({
    watershedSelect: ['Fitzsimmons Creek', 'Watershed 2', 'Harrison (Lower)']

  }),
  mounted () {
  },
  beforeDestroy () {
  }
}
</script>

<style>
  .v-list-item__content, .v-select__selection{
    text-transform: capitalize;
  }
  #surfaceWaterDesign .info-blue .v-icon{
    color: teal;
  }
  #surfaceWaterDesign .v-card__title{
    font-size: 1rem
  }
  #surfaceWaterDesign .v-alert{
    font-size: .9rem
  }
</style>
