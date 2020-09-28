
<template>
  <v-simple-table>
    <template v-slot:default>
      <thead>
      <tr>
        <th class="text-left">Licence Number</th>
        <th class="text-left">Licence Status</th>
        <th class="text-left">Primary Licensee</th>
        <th class="text-left">Source</th>
        <th class="text-left">Licence Quantity</th>
        <th class="text-left">Quantity Unit</th>
        <th class="text-right">Quantity (m³/s)</th>
        <th class="text-right">Quantity (m³/year)</th>
        <th class="text-right">Quantity Flag</th>
      </tr>
      </thead>
      <tbody>
      <tr @mouseenter="onMouseEnterListItem(item)" v-for="(item, i) in licences" :key="uniqueKey(item, i)">
        <td>
          <a :href="`https://j200.gov.bc.ca/pub/ams/Default.aspx?PossePresentation=AMSPublic&amp;PosseObjectDef=o_ATIS_DocumentSearch&amp;PosseMenuName=WS_Main&Criteria_LicenceNumber=${item.properties.fileNumber}`"
             target="_blank"
             rel="noopener">
          {{ item.properties.fileNumber }}
          </a>
        </td>
        <td>{{ item.properties.status }}</td>
        <td>{{ item.properties.licensee }}</td>
        <td>{{ item.properties.source }}</td>
        <td>{{ item.properties.quantity }}</td>
        <td>{{ item.properties.quantityUnits }}</td>
        <td class="text-right">{{ item.properties.quantityPerSec ? item.properties.quantityPerSec.toFixed(6) : null }}</td>
        <td class="text-right">{{ item.properties.quantityPerYear ? item.properties.quantityPerYear.toFixed(0) : null }}</td>
        <td class="text-right">{{ item.properties.quantityFlag }}</td>
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
  methods: {
    onMouseEnterListItem (feature, layerName) {
      feature['display_data_name'] = 'water_rights_licences'
      this.$store.commit('map/updateHighlightFeatureData', feature)
    },
    uniqueKey (lic, i) {
      return lic.properties.fileNumber +
        lic.properties.source +
        lic.properties.quantityPerSec + i
    }
  },
  mounted () {
  },
  beforeDestroy () {
  }
}
</script>

<style>
</style>
