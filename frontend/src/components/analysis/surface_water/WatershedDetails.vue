<template>
  <v-card flat>
    <v-card-text>
      <v-row>
        <v-alert tile color="" dense class="ma-3" width="100%" text
          v-if="modelOutputs && modelOutputs.sourceDescription">
          {{ modelOutputs.sourceDescription }}
        </v-alert>
        <ModelExplanations/>
      </v-row>

      <v-row>
        <v-col>
          <v-card flat outlined tile>
            <v-card-title>
              Drainage area
              <Dialog v-bind="wmd.drainageArea"/>
            </v-card-title>
            <v-card-text class="info-blue">
              <span v-if="watershedDetails.drainage_area">
                {{ watershedDetails.drainage_area.toFixed(2) }}
                <strong>km²</strong>
              </span>
              <span v-else>
                {{ noValueText }}
              </span>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-card flat >
          <v-card-title>
            Mean Annual Discharge
            <Dialog v-bind="wmd.meanAnnualDischarge"/>
          </v-card-title>
          <v-card-text class="info-blue">
            <span v-if="modelOutputs.mad">
              {{ modelOutputs.mad }}
              <strong>m³/s</strong>
            </span>
            <span v-else>
              {{ noValueText }}
            </span>
          </v-card-text>
        </v-card>
        <v-divider vertical></v-divider>
        <v-card flat >
          <v-card-title>
            Total Annual Quantity
            <Dialog v-bind="wmd.totalAnnualQuantity"/>
          </v-card-title>
          <v-card-text class="info-blue">
            <span v-if="availabilityPlotData">
              {{ this.availabilityPlotData.reduce((a, b) => a + b, 0)
                                          .toLocaleString('en', {maximumFractionDigits: 0}) }}
              <strong>m³</strong>
            </span>
            <span v-else>
              {{ noValueText }}
            </span>
          </v-card-text>
        </v-card>
      </v-row>
      <v-divider></v-divider>
      <v-row>
        <v-card flat >
          <v-card-title>
            Mean Annual Runoff
            <Dialog v-bind="wmd.meanAnnualRunoff"/>
          </v-card-title>
          <v-card-text class="info-blue">
            <span v-if="modelOutputs.mar">
              {{ modelOutputs.mar }}
              <strong>
                l/s/km²
              </strong>
            </span>
            <span v-else>{{ noValueText }}</span>
          </v-card-text>
        </v-card>
        <v-divider vertical></v-divider>
        <v-card flat >
          <v-card-title>
            Low7Q2
            <Dialog v-bind="wmd.low7Q2"/>
          </v-card-title>
          <v-card-text class="info-blue">
            <span v-if="modelOutputs.low7q2">
              {{ modelOutputs.low7q2 }}
              <strong>m³</strong>
            </span>
            <span v-else>{{ noValueText }}</span>
          </v-card-text>
        </v-card>
        <v-divider vertical></v-divider>

        <v-card flat >
          <v-card-title>
            Dry7Q10
            <Dialog v-bind="wmd.dry7Q10"/>
          </v-card-title>
          <v-card-text class="info-blue">
            <span v-if="modelOutputs.dry7q10">
              {{ modelOutputs.dry7q10 }}
              <strong>m³/s</strong>
            </span>
            <span v-else>{{ noValueText }}</span>
          </v-card-text>
        </v-card>
      </v-row>
      <v-divider></v-divider>
      <v-row>
        <v-card flat >
          <v-card-title>
            Annual Precipitation
            <Dialog v-bind="wmd.annualPrecipitation"/>
          </v-card-title>
          <v-card-text class="info-blue">
            <span v-if="watershedDetails.annual_precipitation">
              {{ watershedDetails.annual_precipitation.toFixed(0) }}
              <strong>mm</strong>
            </span>
            <span v-else>{{ noValueText }}</span>
          </v-card-text>
        </v-card>
        <v-divider vertical></v-divider>
        <v-card flat >
          <v-card-title>
            Glacial Coverage
            <Dialog v-bind="wmd.glacialCoverage"/>
          </v-card-title>
          <v-card-text class="info-blue">
            <span v-if="watershedDetails.glacial_coverage">
              {{ watershedDetails.glacial_coverage.toFixed(2) }}
            </span>
            <span v-else>{{ noValueText }}</span>
          </v-card-text>
        </v-card>
        <v-divider vertical></v-divider>

        <v-card flat >
          <v-card-title>
            Median Elevation
            <Dialog v-bind="wmd.medianElevation"/>
          </v-card-title>
          <v-card-text class="info-blue">
            <span v-if="watershedDetails.median_elevation">
              {{ watershedDetails.median_elevation.toFixed(0) }}
              <strong>mASL</strong>
            </span>
            <span v-else>{{ noValueText }}</span>
          </v-card-text>
        </v-card>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex'

import Dialog from '../../common/Dialog'
import { WatershedModelDescriptions } from '../../../constants/descriptions'
import ModelExplanations from './ModelExplanations'

export default {
  name: 'WatershedDetails',
  components: {
    Dialog,
    ModelExplanations
  },
  props: ['modelOutputs'],
  data: () => ({
    watershedLoading: false,
    error: null,
    noValueText: 'No info available',
    wmd: WatershedModelDescriptions
  }),
  computed: {
    ...mapGetters('map', ['map']),
    ...mapGetters('surfaceWater', ['availabilityPlotData', 'watershedDetails']),
  },

  mounted () {
  },
  beforeDestroy () {
  }
}
</script>
