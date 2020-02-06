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
                    :headers="[{ text: getMapLayer(name).label, value: 'col1' }]"
                    :items="value.map((x,i) => ({col1: x.properties[getMapLayer(name).label_column], id: i}))"
                    :items-per-page="10"
                    :hide-default-footer="value.length < 10"
                  >
                    <template v-slot:item="{ item }">
                      <v-hover v-slot:default="{ hover }" v-bind:key="`list-item-{$value}${item.id}`">
                        <v-card
                          class="px-2 py-3 mx-1 my-2"
                          :elevation="hover ? 2 : 0"
                          @mousedown="setSingleListFeature(value[item.id], name)"
                          @mouseenter="onMouseEnterListItem(value[item.id], name)"
                        >
                          <span>{{ item.col1 }}</span>
                        </v-card>
                      </v-hover>
                      <v-divider :key="`divider-${item.id}`"></v-divider>
                    </template>
                  </v-data-table>
              </v-list-item-content>
            </v-list-item>
        </v-list-group>
      </div>
    </v-list>
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
    pdfReportLoading: false
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
      this.$store.commit('updateHighlightFeatureData', feature)
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
      console.log('msf')
      this.$router.push('/')
    }
  }
}
</script>

<style>
</style>
