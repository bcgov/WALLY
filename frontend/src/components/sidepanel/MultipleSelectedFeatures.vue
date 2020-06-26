<template>
  <v-card class="elevation-0">
    <v-card-text>

      <span class="float-right mt-3">
        <v-btn
          v-if="dataMartFeatures && dataMartFeatures.length"
          dark
          @click="createSpreadsheetFromSelection"
          color="blue"
        >
          Excel
          <v-icon class="ml-1" v-if="!spreadsheetLoading">cloud_download</v-icon>
          <v-progress-circular
            v-if="spreadsheetLoading"
            indeterminate
            size=24
            class="ml-1"
            color="primary"
          ></v-progress-circular>
        </v-btn>
      </span>
      <div class="title">Selected points
      </div>
      <v-list class="mt-5">
        <div v-for="(dataMartFeature, index) in selectedFeaturesList" :key="`objs-${index}`">

          <!--
          Using value=0 in v-list-group defaults the collapsable list item to "closed".
          In this case, keep the list items collapsed unless there is only one to display.
            -->
          <v-list-group v-for="(value, name) in dataMartFeature" :key="`layerGroup-${value}${name}`" :value="false">
            <template v-slot:activator>
              <v-list-item-content>
                <v-list-item-title>{{getMapLayer(name).display_name}} ({{value.length}} found in area)</v-list-item-title>
              </v-list-item-content>
            </template>
              <v-list-item>
                <v-list-item-content>
                    <v-data-table
                      dense
                      :headers="getHeaders(name)"
                      :items="getItems(name, value)"
                      :items-per-page="10"
                      :hide-default-footer="value.length < 10"
                    >
                      <template v-slot:item="{ item, index }">
                        <tr @mouseenter="onMouseEnterListItem(value[index])" @mousedown="setSingleListFeature(value[index], name)">
                          <td class="v-data-table__divider pa-2" v-for="header in getHeaders(name)" :key="`td-${name}-${header.value}`">{{ item[header.value] }}</td>
                        </tr>
                      </template>
                    </v-data-table>
                </v-list-item-content>
              </v-list-item>
          </v-list-group>
        </div>
      </v-list>
      <div v-if="selectedFeaturesList && !selectedFeaturesList.length">
        Select a map feature or draw a polygon to browse data.
      </div>
    </v-card-text>

  </v-card>
</template>

<script>
import { mapGetters } from 'vuex'
import EventBus from '../../services/EventBus'
export default {
  name: 'MultipleSelectedFeatures',
  data: () => ({
    spreadsheetLoading: false,
    pdfReportLoading: false,
    wellheaders: [
      { text: 'Well Tag No.', value: 'well_tag_number', align: 'start', divider: true },
      { text: 'Well Identification Plate No.', value: 'identification_plate_number', align: 'start', divider: true },
      { text: 'Street Address', value: 'street_address', align: 'start', divider: true }
    ],
    aquiferHeaders: [
      { text: 'Aquifer Name', value: 'NAME', align: 'start', divider: true },
      { text: 'Aquifer Number', value: 'AQUIFER_ID', align: 'center', divider: true },
      { text: 'Aquifer Material', value: 'MATERIAL', align: 'center', divider: true },
      { text: 'Aquifer Subtype', value: 'SUBTYPE', align: 'start', divider: true }
    ]
  }),
  computed: {
    ...mapGetters('map', ['getMapLayer']),
    ...mapGetters(['dataMartFeatures', 'selectionBoundingBox']),
    selectedFeaturesList () {
      const selection = this.dataMartFeatures
      const filtered = selection.filter((x) => {
        // selections come back as an array of objects (one for each layer), and if the layer has features
        // present in the user selection, the object should have a key (named after the layer)
        // with an array of features.
        return !!Object.entries(x).filter((kv) => {
          // this checks for at least one key/value pair that has a non-empty array.
          // in other words, we are looking for a key/value pair that has an array of features.
          return kv[1] && kv[1].length
        }).length
      })

      // return an array of only the layers that contain selected features.
      return filtered
    }
  },
  methods: {
    getHeaders(display_name) {
      if (display_name === 'groundwater_wells') {
        return this.wellheaders
      } else if (display_name === 'aquifers') {
        return this.aquiferHeaders
      } else {
        return [{ text: this.getMapLayer(display_name).label, value: 'col1' }]
      }
    },
    getItems(display_name, features) {
      if (display_name === 'groundwater_wells' ||
          display_name === 'aquifers') {
        return features.map(f => f.properties)
      } else {
        return features.map((x,i) => ({col1: x.properties[this.getMapLayer(display_name).label_column], id: i}))
      }
    },
    setSingleListFeature (item, displayName) {
      this.$store.commit('setDataMartFeatureInfo',
        {
          type: item.type,
          display_data_name: displayName,
          geometry: item.geometry,
          properties: item.properties
        })
    },
    onMouseEnterListItem (feature, layerName) {
      feature['display_data_name'] = layerName
      this.$store.commit('map/updateHighlightFeatureData', feature)
    },
    createSpreadsheetFromSelection () {
      this.spreadsheetLoading = true
      this.$store.dispatch('downloadExcelReport',
        {
          format: 'xlsx',
          polygon: JSON.stringify(this.selectionBoundingBox.geometry.coordinates || []),
          layers: this.dataMartFeatures.map((feature) => {
            // return the layer names from the active data mart features as a list.
            // there is only expected to be one key, so we could use either
            // Object.keys(feature)[0] or call flat() on the resulting nested array.
            return Object.keys(feature)
          }).flat()
        }
      ).catch((e) => {
        EventBus.$emit('error', true)
      }).finally(() => {
        this.spreadsheetLoading = false
      })
    }
  },
  mounted () {
    if (!this.dataMartFeatures || !this.dataMartFeatures.length) {
      this.$router.push('/')
    }
  },
  beforeDestroy () {
  }
}
</script>

<style>
  .v-list-item__content, .v-select__selection {
    text-transform: none;
  }
</style>
