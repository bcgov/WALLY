<template>
  <v-container id="surfaceWaterDesign">
    <v-toolbar flat>
      <v-banner color="indigo"
                icon="mdi-chart-bar"
                icon-color="white"
                width="100%"
      >
        <v-toolbar-title>
          Surface water availability
        </v-toolbar-title>
      </v-banner>
    </v-toolbar>
    <v-row>
      <v-col class="pb-0">
        <v-alert type="info" dense class="mb-0" outlined dismissible>
            This modelling output has not been peer reviewed and is still considered
            experimental. Use the values generated with your own discretion.
        </v-alert>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-btn-toggle>
          <v-btn outlined small
                 color="primary" class="">
            <span class="hidden-sm-and-down">
            See on map
            </span>
          </v-btn>
          <v-menu bottom right>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                small
                dark
                icon
                v-bind="attrs"
                v-on="on"
              >
                <v-icon>layers</v-icon>
              </v-btn>
            </template>
            <v-card class="pa-5">
              <v-checkbox small label="Hydrometric Stations" class="mt-0"/>
              <v-checkbox small label="Water Rights Applications" class="mt-0"/>
              <v-checkbox small label="Water Rights Licences" class="mt-0"/>
              <v-checkbox small label="Known BC Fish Observations & Distributions" class="mt-0"/>
              <v-checkbox small label="Water Approval Points" class="mt-0"/>
            </v-card>
          </v-menu>

        </v-btn-toggle>
      </v-col>
      <v-col>
      </v-col>
      <v-col class="text-right">
        <v-btn-toggle>
        <v-btn outlined small
         color="primary" class="">
            <span class="hidden-sm-and-down">
            Export
            </span>
        </v-btn>
        <v-menu bottom right>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              small
              dark
              icon
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>expand_more</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item>
              <v-list-item-title>
                PDF
                <v-icon class="ml-1">cloud_download</v-icon>
              </v-list-item-title>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>
               Excel
                <v-icon class="ml-1">cloud_download</v-icon>
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>

        </v-btn-toggle>
      </v-col>
    </v-row>
    <v-card flat>
      <v-select
        :items="watershedSelect"
        :menu-props="{ maxHeight: '400' }"
        label="Watershed"
        item-text="label"
        item-value="value"
        hint="Select from available watersheds at this location"
      ></v-select>
    </v-card>
    <v-card>
      <v-tabs
        vertical
        v-model="tab"
        background-color="blue darken-4"
        dark
        show-arrows
      >
        <v-tab class="text-left">
          Watershed
        </v-tab>
        <v-tab class="text-left">
          Monthly Discharge
        </v-tab>
        <v-tab class="text-left">
          Licenced Quantity
        </v-tab>
        <v-tab class="text-left">
          Hydrometric Stations
        </v-tab>
        <v-tab>
          Streamflow Report
        </v-tab>
        <v-tab class="text-left">
          Fish Observations
        </v-tab>
        <v-tab class="text-left">
         FIDQ
        </v-tab>
        <v-tab>
           Runoff Models
        </v-tab>

        <!-- Watershed -->
        <v-tab-item>
          <WatershedDetails></WatershedDetails>

        </v-tab-item>
        <!-- Licenced Quantity -->
        <v-tab-item>
          <MonthlyDischarge></MonthlyDischarge>
        </v-tab-item>
        <v-tab-item>
          <WatershedLicencedQuantity></WatershedLicencedQuantity>
        </v-tab-item>

        <!-- Hydrometric Stations -->
        <v-tab-item>
          <HydrometricStations></HydrometricStations>
        </v-tab-item>

        <!-- Inventory of Streamflow Reports -->
        <v-tab-item>
          <InventoryofStreamflowReport></InventoryofStreamflowReport>
        </v-tab-item>

        <!-- Fish Observations -->
        <v-tab-item>
          <FishObservations></FishObservations>
        </v-tab-item>

        <!-- FIDQ -->
        <v-tab-item>
          <FIDQ></FIDQ>
        </v-tab-item>

        <!-- Comparative Runoff Models -->
        <v-tab-item>
          <ComparativeRunoffModels/>
        </v-tab-item>
      </v-tabs>
    </v-card>
  </v-container>
</template>

<script>
import WatershedDetails from './WatershedDetails'
import WatershedLicencedQuantity from './WatershedLicencedQuantity'
import HydrometricStations from './HydrometricStations'
import InventoryofStreamflowReport from './InventoryofStreamflowReport'
import FishObservations from './FishObservations'
import ComparativeRunoffModels from './ComparativeRunoffModels'
import MonthlyDischarge from './MonthlyDischarge'
import FIDQ from './FIDQ'
export default {
  name: 'WatershedDesign',
  components: {
    FIDQ,
    MonthlyDischarge,
    HydrometricStations,
    WatershedDetails,
    WatershedLicencedQuantity,
    InventoryofStreamflowReport,
    FishObservations,
    ComparativeRunoffModels
  },
  data: () => ({
    watershedSelect: ['Fitzsimmons Creek', 'Watershed 2', 'Harrison (Lower)'],
    infoTabs: null,
    watershedLoading: false,
    selectedWatershed: null,
    assessmentWatershed: null,
    hydrometricWatershed: null,
    watersheds: [],
    geojsonLayersAdded: [],
    includePOIPolygon: false,
    watershedDetailsLoading: false,
    spreadsheetLoading: false,
    show: {
      editingModelInputs: false
    },
    tab: null,
    items: [
      {
        tab: 'Watershed',
        content: 'Watershed'
      },
      {
        tab: 'Licenced Quantity',
        content: 'Blah'
      },
      {
        tab: 'Hydrometric Stations',
        content: 'Lada'
      },
      {
        tab: 'Fish Observations',
        content: 'Fish'
      },
      {
        tab: 'Comparative Runoff Models',
        content: 'Fish'
      }
    ]
  }),
  watch: {
  },
  computed: {
  },
  methods: {
  },
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
