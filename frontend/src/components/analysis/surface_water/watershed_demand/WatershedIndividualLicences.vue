
<template>
  <v-simple-table>
    <template v-slot:default>
      <thead>
      <tr>
        <th class="text-left">Licence Number</th>
        <th class="text-left">Licence Status</th>
        <th class="text-left">Primary Licensee</th>
        <th class="text-left">Source</th>
        <th class="text-left">Quantity (m³/s)</th>
        <th class="text-left">Quantity (m³/year)</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="item in licences" :key="item.name">
        <td>
          <a href="https://j200.gov.bc.ca/pub/ams/Default.aspx?PossePresentation=AMSPublic&PosseObjectDef=o_ATIS_DocumentSearch&PosseMenuName=WS_Main&Criteria_LicenceNumber=C116806">
          {{ item.number }}
          </a>
        </td>
        <td>{{ item.status }}</td>
        <td>{{ item.licensee }}</td>
        <td>{{ item.source }}</td>
        <td>{{ item.quantity_s }}</td>
        <td>{{ item.quantity_y }}</td>
      </tr>
      </tbody>
    </template>
  </v-simple-table>
</template>

<script>
export default {
  name: 'WatershedIndividualLicences',
  components: {
  },
  props: ['licences'],
  data: () => ({
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
</style>