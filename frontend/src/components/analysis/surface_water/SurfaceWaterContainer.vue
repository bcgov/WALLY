<template>
  <v-container>
    <v-toolbar flat>
      <v-banner color="indigo"
                icon="mdi-chart-bar"
                icon-color="white"
                width="100%"
      >
        <v-toolbar-title>
          Analyze surface water availability
        </v-toolbar-title>
      </v-banner>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn icon v-on="on" v-on:click="exitFeature">
            <v-icon>close</v-icon>
          </v-btn>
        </template>
        <span>Exit</span>
      </v-tooltip>
    </v-toolbar>
    <div
    v-if="pointOfInterest && pointOfInterest.display_data_name === 'point_of_interest'">
      <SurfaceWaterV2 v-if="this.app.config && this.app.config.surface_water_design_v2"></SurfaceWaterV2>
      <SurfaceWater v-else></SurfaceWater>
    </div>
    <v-row class="mt-3" v-else>
      <v-col cols=12 lg=8>
        <p class="pl-3">Select a point of interest to determine water availability.</p>
      </v-col>
      <v-col class="text-right">
        <v-btn @click="selectPointOfInterest" color="primary" outlined>Select a point</v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <div class="headline">Instructions, Methodology, and Data Sources</div>
        <div class="title my-3 font-weight-bold">Instructions</div>
          <ol>
            <li>Zoom into an area of interest on the map.</li>
            <li>Click the “Select Point” button and drop a point of interest on the map.</li>
            <li>Choose different watersheds in the area for analysis from the drop down menu.</li>
            <li>After the analysis is produced, an "Export" button allows you to download all the information from all the tabs into Excel or PDF.</li>
            <li>The "Model Calculations and Error" information box describes the model's calculations, coefficients table, and relevancy to watershed.</li>
            <li>Below the initial outputs, the "Model Inputs" button allows you to customize the model inputs values for expert adjustment and discretion.</li>
            <li>A secondary "Download Watershed Info" button will download all the outputs values into a PDF.</li>
            <li>In the fourth tab for "Licenced Quantity", the "Monthly allocation coefficients" button allows you to edit the monthly allocation coefficient values by re-distributing the expected annual proportion of licensed water quantity. A secondary button allows you to hide or show the Water Rights Licences layer in the map.</li>
            <li>In the top section, the "Reset" button will clear your previous analysis.</li>
            <li>If no analysis is produced, then press "Select A Point" and try again. It also helps to have the map zoomed to a smaller area with a sufficiently large amount of detail.</li>
          </ol>

        <div class="title my-3 font-weight-bold">Methodology</div>

        <p>
          Disclaimer: This modelling output has not been peer reviewed and is still considered experimental. Use the values generated with your own discretion.
        </p>

        <p>
          The Surface Water Availability analysis automatically defaults to the "Estimated Catchment Area". To determine what area was used in the analysis, refer to the map to see the polygon outline.
        </p>

        <p>
          The outputs provided for the "Estimated Catchment Area" are for the total watershed, starting from the point of interest and upstream. This area is comprised of all of the Freshwater Atlas (FWA) Watershed polygons that are located upstream of the point of interest based on each polygon's watershed code and local watershed code. The watershed polygon that contains the point of interest is included. Depending on where the point of interest is placed, there may be surface area downstream, but not additional tributaries. You can turn on the Freshwater Atlas Watersheds layer from the WALLY layer library to be more clear on what is included within the catchment area and then double check the catchment area that was automatically delineated is what you want.
        </p>

        <p>
          It is all the small watershed polygons that make up the area that drains toward the point of interest. If there are any catchment polygons that aren't highlighted, it should mean that they don't drain to the point of interest. If you looking at an area that appears to straddle two FWA polygons, you can try to place a point of interest near the streams in the area to see which watersheds come back.
        </p>

        <p>
          The outputs in this analysis are based on the South Coast Stewardship Baseline model from Sentlinger, 2016. This model is only available for the South Coast region. Additional models are currently being scoped to support additional regions. While model estimates, such as mean annual discharge and monthly distributions, are not presently provided for regions outside of the South Coast, you can still view other data, such as water rights licences, fish information, and links to EcoCat for streamflow reports.
        </p>

        <div class="title my-3 font-weight-bold">Data Sources</div>

        <p>
          The Surface Water Availability analysis feature uses the following datasets:
        </p>
          <ul>
            <li>
              <a href="https://catalogue.data.gov.bc.ca/dataset/freshwater-atlas-assessment-watersheds">Freshwater Atlas Assessment Watersheds</a>
            </li>
            <li>
              <a href="https://catalogue.data.gov.bc.ca/dataset/freshwater-atlas-named-watersheds">Freshwater Atlas Named Watersheds</a>
            </li>
            <li>
              <a href="https://catalogue.data.gov.bc.ca/dataset/freshwater-atlas-stream-network">Freshwater Atlas Watersheds</a>
            </li>
            <li>
              <a href="https://a100.gov.bc.ca/pub/acat/public/welcome.do">EcoCat Reports</a>
            </li>
            <li>
              <a href="https://catalogue.data.gov.bc.ca/dataset/hydrology-normal-annual-runoff-isolines-1961-1990-historical">Hydrology: Normal Annual Runoff Isolines (1961 - 1990) - Historical</a>
            </li>
            <li>
              <a href="https://catalogue.data.gov.bc.ca/dataset/hydrology-hydrometric-watershed-boundaries">Hydrology: Hydrometric Watershed Boundaries</a>
            </li>
            <li>
              <a href="https://www.canada.ca/en/environment-climate-change/services/water-overview/quantity/monitoring/survey/data-products-services/national-archive-hydat.html">National Water Data Archive (HYDAT)</a>
            </li>
            <li>
              <a href="https://catalogue.data.gov.bc.ca/dataset/known-bc-fish-observations-and-bc-fish-distributions">Known BC Fish Observations and BC Fish Distributions</a>
            </li>
            <li>
              <a href="http://a100.gov.bc.ca/pub/fidq/welcome.do">Fish Inventories Data Queries (FIDQ)</a>
            </li>
            <li>
              <a href="https://catalogue.data.gov.bc.ca/dataset/water-rights-licences-public">Water Rights Licences - Public</a>
            </li>
          </ul>
        <p class="mt-3">
          If you notice an issue with data or layers, please notify the contact email listed in the URLs above.
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import SurfaceWater from './SurfaceWater'
import SurfaceWaterV2 from './SurfaceWaterV2'

export default {
  name: 'SurfaceWaterContainer',
  components: {
    SurfaceWater,
    SurfaceWaterV2
  },
  data: () => ({
    licencesLayerAutomaticallyEnabled: false,
    hydatLayerAutomaticallyEnabled: false,
    applicationsLayerAutomaticallyEnabled: false,
    fishLayerAutomaticallyEnabled: false,
    approvalLayerAutomaticallyEnabled: false
  }),
  methods: {
    enableApplicationsLayer () {
      this.$store.dispatch('map/addMapLayer', 'water_rights_applications')
    },
    disableApplicationsLayer () {
      this.$store.dispatch('map/removeMapLayer', 'water_rights_applications')
    },
    enableLicencesLayer () {
      this.$store.dispatch('map/addMapLayer', 'water_rights_licences')
    },
    disableLicencesLayer () {
      this.$store.dispatch('map/removeMapLayer', 'water_rights_licences')
    },
    enableHydatLayer () {
      this.$store.dispatch('map/addMapLayer', 'hydrometric_stream_flow')
    },
    disableHydatLayer () {
      this.$store.dispatch('map/removeMapLayer', 'hydrometric_stream_flow')
    },
    enableFishLayer () {
      this.$store.dispatch('map/addMapLayer', 'fish_observations')
    },
    disableFishLayer () {
      this.$store.dispatch('map/removeMapLayer', 'fish_observations')
    },
    enableApprovalsLayer () {
      this.$store.dispatch('map/addMapLayer', 'water_approval_points')
    },
    disableApprovalsLayer () {
      this.$store.dispatch('map/removeMapLayer', 'water_approval_points')
    },
    loadSurfaceWaterAnalysis () {
      if (!this.isHydatLayerEnabled) {
        this.hydatLayerAutomaticallyEnabled = true
        this.enableHydatLayer()
      }
      if (!this.isApplicationsLayerEnabled) {
        this.applicationsLayerAutomaticallyEnabled = true
        this.enableApplicationsLayer()
      }
      if (!this.isLicencesLayerEnabled) {
        this.licencesLayerAutomaticallyEnabled = true
        this.enableLicencesLayer()
      }
      if (!this.isFishLayerEnabled) {
        this.fishLayerAutomaticallyEnabled = true
        this.enableFishLayer()
      }
      if (!this.isApprovalsLayerEnabled) {
        this.approvalLayerAutomaticallyEnabled = true
        this.enableApprovalsLayer()
      }
      this.loadFeature()
    },
    loadFeature () {
      if ((!this.pointOfInterest || !this.pointOfInterest.geometry) && this.$route.query.coordinates) {
        // load feature from coordinates
        const coordinates = this.$route.query.coordinates.map((x) => Number(x))

        let data = {
          coordinates: coordinates,
          layerName: 'point-of-interest'
        }

        this.$store.dispatch('map/addFeaturePOIFromCoordinates', data)
      }
    },
    ...mapActions('map', ['setDrawMode', 'clearSelections', 'selectPointOfInterest']),
    ...mapActions(['exitFeature'])
  },
  computed: {
    isLicencesLayerEnabled () {
      return this.isMapLayerActive('water_rights_licences')
    },
    isApplicationsLayerEnabled () {
      return this.isMapLayerActive('water_rights_applications')
    },
    isHydatLayerEnabled () {
      return this.isMapLayerActive('hydrometric_stream_flow')
    },
    isFishLayerEnabled () {
      return this.isMapLayerActive('fish_observations')
    },
    isApprovalsLayerEnabled () {
      return this.isMapLayerActive('water_approval_points')
    },
    ...mapGetters('map', ['isMapLayerActive', 'isMapReady']),
    ...mapGetters(['pointOfInterest', 'app'])
  },
  watch: {
    pointOfInterest (value) {
      if (value && value.geometry) {
        // Update router
        global.config.debug && console.log('[wally] updating POI route')
        this.$router.push({
          query: { ...this.$route.query, coordinates: value.geometry.coordinates }
        })
      }
    },
    isMapReady (value) {
      if (value) {
        this.clearSelections()
        this.loadSurfaceWaterAnalysis()
      }
    }
  },
  mounted () {
    this.loadSurfaceWaterAnalysis()
  },
  beforeDestroy () {
    if (this.hydatLayerAutomaticallyEnabled) {
      this.disableHydatLayer()
    }
    if (this.licencesLayerAutomaticallyEnabled) {
      this.disableLicencesLayer()
    }
    if (this.applicationsLayerAutomaticallyEnabled) {
      this.disableApplicationsLayer()
    }
    if (this.fishLayerAutomaticallyEnabled) {
      this.disableFishLayer()
    }
    if (this.approvalLayerAutomaticallyEnabled) {
      this.disableApprovalsLayer()
    }
  }
}
</script>

<style>

</style>
