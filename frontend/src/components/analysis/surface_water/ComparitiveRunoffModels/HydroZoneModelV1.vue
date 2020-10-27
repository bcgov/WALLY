<template>
  <div>
    <v-card-text v-if="showWallyModelFeatureFlag && hydrologicalZoneModelRunoff">
      <v-card-actions>
        <v-card-subtitle class="pr-0 pl-2 pr-2">
          Source:
        </v-card-subtitle>
        Wally Hydrological Zone Model V1
      </v-card-actions>
      <v-row class="pl-3 pr-3">
        <v-col>
          <v-card flat outlined tile height="100%">
            <v-card-title>
              Mean Annual Runoff Estimate:
              <v-icon small class="ml-1">mdi-information-outline</v-icon>
            </v-card-title>
            <v-card-text class="info-blue">
              <strong>{{ hydrologicalZoneModelRunoff }} m^3/sec</strong>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col>
          <v-card flat outlined tile height="100%">
            <v-card-title>
              Model R Squared:
              <v-icon small class="ml-1">mdi-information-outline</v-icon>
            </v-card-title>
            <v-card-text class="info-blue">
              <strong>{{ hydrologicalZoneModelRSquared }}</strong>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-card-text>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'HydroZoneModelV1',
  components: {
  },
  props: {
    model_output: {}
  },
  data: () => ({
  }),
  computed: {
    ...mapGetters('surfaceWater', ['watershedDetails']),
    hydrologicalZoneModelRunoff () {
      if (!this.watershedDetails || !this.watershedDetails.wally_hydro_zone_model_output_v1 ||
        !this.watershedDetails.wally_hydro_zone_model_output_v1.mean_annual_flow) {
        return null
      }
      return (Number(this.watershedDetails.wally_hydro_zone_model_output_v1.mean_annual_flow)).toFixed(2)
    },
    hydrologicalZoneModelRSquared () {
      if (!this.watershedDetails || !this.watershedDetails.wally_hydro_zone_model_output_v1 ||
        !this.watershedDetails.wally_hydro_zone_model_output_v1.r_squared) {
        return null
      }
      return (Number(this.watershedDetails.wally_hydro_zone_model_output_v1.r_squared)).toFixed(2)
    }
  },
  methods: {
    showWallyModelFeatureFlag () {
      return this.app && this.app.config && this.app.config.wally_model
    }
  },
  mounted () {
  }
}
</script>

<style>
</style>
