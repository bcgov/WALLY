<template>
  <v-card flat>
    <v-card-title
      class="title mt-5 ml-3 mr-3 pa-1 mb-2"
      dark>
      Watershed Licenced Quantity
    </v-card-title>
    <v-card-text>
      <h3>Water Rights Licences</h3>
      <v-row>
        <v-col>
        <v-card flat outlined tile>
          <v-card-title>
            Total annual licenced quantity
            <v-icon small class="ml-1">mdi-information-outline</v-icon>
          </v-card-title>
          <v-card-text class="info-blue">
            <strong>000000.00 m³/s</strong>
          </v-card-text>
        </v-card>
        </v-col>
      </v-row>
      <v-data-table
        :headers="headers"
        :items="useTypes"
        :single-expand="singleExpand"
        :expanded.sync="expanded"
        item-key="useType"
        show-expand
        class="elevation-1"
      >
        <template v-slot:top>
          <v-toolbar flat>
          <h4>Annual licenced quantity by use type</h4>
          </v-toolbar>
        </template>
        <template v-slot:expanded-item="{ headers, item }">
          <td :colspan="headers.length">
            <WatershedIndividualLicences/>
<!--            More info about {{ item.useType }}-->
          </td>
        </template>
      </v-data-table>
      <v-card-actions>
        <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" small depressed light>
            <v-icon small color="primary">
              mdi-tune
            </v-icon>
            Monthly allocation coefficients
          </v-btn>
        </template>
        <span>Configure monthly allocation coefficients</span>
      </v-tooltip>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" small  depressed light class="ml-2">
              <v-icon small>
               layers
              </v-icon>
             Hide points on map
            </v-btn>
          </template>
          <span>Hide Water Rights Licences Layer</span>
        </v-tooltip>
      </v-card-actions>

      <v-divider class="mt-8 mb-8"></v-divider>
      <!-- Water approval points -->
      <h3>Water Approval Points (Short Term Licences)</h3>
      <v-row>
        <v-col>
          <v-card flat outlined tile>
            <v-card-title>
              Total annual approved quantity
              <v-icon small class="ml-1">mdi-information-outline</v-icon>
            </v-card-title>
            <v-card-text class="info-blue">
              <strong>000000.00 m³/year</strong>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-data-table
        :headers="approvalHeaders"
        :items="approvalPoints"
        item-key="useType"
        class="elevation-1"
      >
        <template v-slot:top>
          <v-toolbar flat>
            <h4>Short Term Water Approval Points</h4>
          </v-toolbar>
        </template>
      </v-data-table>
      <v-card-actions>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" small depressed light>
              <v-icon small color="primary">
                mdi-tune
              </v-icon>
              Monthly allocation coefficients
            </v-btn>
          </template>
          <span>Configure short term monthly allocation coefficients</span>
        </v-tooltip>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" small  depressed light class="ml-2">
              <v-icon small>
                layers
              </v-icon>
              Hide points on map
            </v-btn>
          </template>
          <span>Hide Water Approval Points Layer</span>
        </v-tooltip>
      </v-card-actions>

      <v-divider class="mt-8 mb-8"></v-divider>
      <!-- Availability vs Licensed Quantity -->
      <h3>Availability vs Licensed Quantity</h3>
      <v-row>
        <v-col>
          <v-card flat outlined tile>
            <v-card-title>
              How to read this graph
<!--              <v-icon small class="ml-1">mdi-information-outline</v-icon>-->
            </v-card-title>
            <v-card-text class="info-blue">
              <strong>
                This graph shows available water after allocation from existing surface water licences, as determined by subtracting licensed quantities (including any adjusted monthly allocation values) from the estimated discharge for each month.
              </strong>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <img src="mockups/available_vs_monthly.png" width="800" />
      </v-row>

<!--      <v-card-actions>-->
<!--        <v-tooltip bottom>-->
<!--          <template v-slot:activator="{ on }">-->
<!--            <v-btn v-on="on" small depressed light>-->
<!--              <v-icon small color="primary">-->
<!--                mdi-tune-->
<!--              </v-icon>-->
<!--              Monthly allocation coefficients-->
<!--            </v-btn>-->
<!--          </template>-->
<!--          <span>Configure short term monthly allocation coefficients</span>-->
<!--        </v-tooltip>-->
<!--        <v-tooltip bottom>-->
<!--          <template v-slot:activator="{ on }">-->
<!--            <v-btn v-on="on" small  depressed light class="ml-2">-->
<!--              <v-icon small>-->
<!--                layers-->
<!--              </v-icon>-->
<!--              Hide points on map-->
<!--            </v-btn>-->
<!--          </template>-->
<!--          <span>Hide Water Approval Points Layer</span>-->
<!--        </v-tooltip>-->
<!--      </v-card-actions>-->
    </v-card-text>
  </v-card>
</template>

<script>
import WatershedIndividualLicences from './WatershedIndividualLicences'
export default {
  name: 'WatershedDetails',
  components: {
    WatershedIndividualLicences
  },
  data: () => ({
    expanded: [],
    singleExpand: false,
    headers: [
      {
        text: 'Use Type',
        value: 'useType'
      },
      {
        text: 'Quantity (m³/s)',
        value: 'quantity',
        align: 'end'
      },
      {
        text: 'Maximum Use (m³/s)',
        value: 'maxUse',
        align: 'end'
      },
      {
        text: 'Minimum Use (m³/s)',
        value: 'minUse',
        align: 'end'
      },
      {
        text: 'Period of Use',
        value: 'periodOfUse',
        align: 'end'
      },
      {
        text: '',
        value: 'data-table-expand'
      }
    ],
    useTypes: [
      {
        useType: 'Grnhouse & Nursery: Nursery (02I22)',
        quantity: '000.00',
        maxUse: '000.00',
        minUse: '000.00',
        periodOfUse: '----'
      },
      {
        useType: 'Irrigation: Private (03B)',
        quantity: '000.00',
        maxUse: '000.00',
        minUse: '000.00',
        periodOfUse: '----'
      },
      {
        useType: 'Lwn, Fairway & Grdn: Watering (02F)',
        quantity: '000.00',
        maxUse: '000.00',
        minUse: '000.00',
        periodOfUse: '----'
      },
      {
        useType: 'Land Improve: General (04A)',
        quantity: '000.00',
        maxUse: '000.00',
        minUse: '000.00',
        periodOfUse: '----'
      },
      {
        useType: 'Domestic (01A)',
        quantity: '000.00',
        maxUse: '000.00',
        minUse: '000.00',
        periodOfUse: '----'
      },
      {
        useType: 'Grnhouse & Nursery: Grnhouse (02I17)',
        quantity: '000.00',
        maxUse: '000.00',
        minUse: '000.00',
        periodOfUse: '----'
      },
      {
        useType: 'Processing & Mfg: Processing (02B)',
        quantity: '000.00',
        maxUse: '000.00',
        minUse: '000.00',
        periodOfUse: '----'
      },
      {
        useType: 'Livestock & Animal: Stockwatering (02I31)',
        quantity: '000.00',
        maxUse: '000.00',
        minUse: '000.00',
        periodOfUse: '----'
      },
      {
        useType: 'Stream Storage: Non-Power (08A)',
        quantity: '000.00',
        maxUse: '000.00',
        minUse: '000.00',
        periodOfUse: '----'
      },
      {
        useType: 'Pond & Aquaculture (02E)',
        quantity: '000.00',
        maxUse: '000.00',
        minUse: '000.00',
        periodOfUse: '----'
      }
    ],
    approvalHeaders: [
      {
        text: 'Approval Number',
        value: 'approvalNumber'
      },
      {
        text: 'Works',
        value: 'works',
        align: 'start'
      },
      {
        text: 'Start Date',
        value: 'startDate',
        align: 'end'
      },
      {
        text: 'Expiry Date',
        value: 'expiryDate',
        align: 'end'
      },
      {
        text: 'Quantity (m³/s)',
        value: 'quantity',
        align: 'end'
      }
    ],
    approvalPoints: [
      {
        approvalNumber: '0000000',
        works: '-----',
        startDate: 'yyyy-mm-dd',
        expiryDate: 'yyyy-mm-dd',
        quantity: '000.00'
      },
      {
        approvalNumber: '0000000',
        works: '-----',
        startDate: 'yyyy-mm-dd',
        expiryDate: 'yyyy-mm-dd',
        quantity: '000.00'
      },
      {
        approvalNumber: '0000000',
        works: '-----',
        startDate: 'yyyy-mm-dd',
        expiryDate: 'yyyy-mm-dd',
        quantity: '000.00'
      },
      {
        approvalNumber: '0000000',
        works: '-----',
        startDate: 'yyyy-mm-dd',
        expiryDate: 'yyyy-mm-dd',
        quantity: '000.00'
      },
      {
        approvalNumber: '0000000',
        works: '-----',
        startDate: 'yyyy-mm-dd',
        expiryDate: 'yyyy-mm-dd',
        quantity: '000.00'
      },
      {
        approvalNumber: '0000000',
        works: '-----',
        startDate: 'yyyy-mm-dd',
        expiryDate: 'yyyy-mm-dd',
        quantity: '000.00'
      },
      {
        approvalNumber: '0000000',
        works: '-----',
        startDate: 'yyyy-mm-dd',
        expiryDate: 'yyyy-mm-dd',
        quantity: '000.00'
      },
      {
        approvalNumber: '0000000',
        works: '-----',
        startDate: 'yyyy-mm-dd',
        expiryDate: 'yyyy-mm-dd',
        quantity: '000.00'
      },
      {
        approvalNumber: '0000000',
        works: '-----',
        startDate: 'yyyy-mm-dd',
        expiryDate: 'yyyy-mm-dd',
        quantity: '000.00'
      },
      {
        approvalNumber: '0000000',
        works: '-----',
        startDate: 'yyyy-mm-dd',
        expiryDate: 'yyyy-mm-dd',
        quantity: '000.00'
      },
      {
        approvalNumber: '0000000',
        works: '-----',
        startDate: 'yyyy-mm-dd',
        expiryDate: 'yyyy-mm-dd',
        quantity: '000.00'
      }
    ]
  }),
  mounted () {
  },
  beforeDestroy () {
  }
}
</script>

<style>
#surfaceWaterDesign .v-card__title.title{
  background-color: teal;
  border-radius: 0;
  color: white;
}
#surfaceWaterDesign .info-blue {
  color: teal;
}
</style>
