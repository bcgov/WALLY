<template>
  <div>
    <v-card-text v-if="showWallyModelFeatureFlag && modelData">
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
              <strong>{{ meanAnnualFlow }} m^3/sec</strong>
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
              <strong>{{ meanAnnualFlowRSquared }}</strong>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-card-text>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import qs from 'querystring'
import ApiService from '../../../../services/ApiService'

export default {
  name: 'HydroZoneModelV1',
  components: {
  },
  props: {
  },
  data: () => ({
    modelLoading: false,
    modelData: {}
  }),
  computed: {
    ...mapGetters('surfaceWater', ['watershedDetails']),
    meanAnnualFlow () {
      if (this.modelData && this.modelData.mean_annual_flow) {
        return Number(this.modelData.mean_annual_flow).toFixed(2)
      }
      return null
    },
    meanAnnualFlowRSquared () {
      if (this.modelData && this.modelData.r_squared) {
        return Number(this.modelData.r_squared).toFixed(2)
      }
      return null
    }
  },
  methods: {
    fetchWatershedModel (details) {
      this.modelLoading = true
      const params = {
        hydrological_zone: details.hydrological_zone,
        drainage_area: details.drainage_area,
        median_elevation: details.median_elevation,
        annual_precipitation: details.annual_precipitation
      }
      console.log(params)
      ApiService.query(`/api/v1/hydrological_zones/v1_watershed_drainage_model?${qs.stringify(params)}`)
        .then(r => {
          this.modelData = r.data
          this.modelLoading = false
        })
        .catch(e => {
          this.modelLoading = false
          console.error(e)
        })
    },
    showWallyModelFeatureFlag () {
      return this.app && this.app.config && this.app.config.wally_model
    }
  },
  mounted () {
  },
  watch: {
    watershedDetails: {
      immediate: true,
      handler (val, oldVal) {
        this.fetchWatershedModel(val)
      }
    }
  }
}
</script>

<style>
</style>
