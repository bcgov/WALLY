<template>
  <div>
    <div class="title my-5">Surficial Geology (Terrain Inventory Mapping)</div>
    <div>
      <p>
        Note: Surficial geology data is based on
        <a href="https://catalogue.data.gov.bc.ca/dataset/terrain-inventory-mapping-tim-detailed-polygons-with-short-attribute-table-spatial-view" target="_blank">
          Terrain Inventory Mapping</a>.
        Data may be incomplete in the area of interest.
      </p>
    </div>
    <div v-if="surficialGeologyLoading">
      <v-progress-linear show indeterminate></v-progress-linear>
    </div>
    <div v-if="surficialGeologyByType">
      <div class="my-5">
        <v-data-table
          :items="surficialGeologyByType"
          :headers="materialHeaders"
          sort-by="area_within_watershed"
          sort-desc
        >
          <template v-slot:item.area_within_watershed="{ item }">
            {{ item.area_within_watershed.toFixed(1) }}
          </template>
        </v-data-table>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import ApiService from '../../../services/ApiService'
export default {
  name: 'SurficialGeology',
  props: ['watershedID', 'record'],
  data: () => ({
    surficialGeologyLoading: false,
    surficialGeologyByType: [],
    materialHeaders: [
      { text: 'Material', value: 'soil_type', sortable: true },
      { text: 'Area within watershed (m3)', value: 'area_within_watershed' }
    ]
  }),
  computed: {
    ...mapGetters('map', ['map'])
  },
  watch: {
    watershedID () {
      this.surficialGeologyByType = []
      this.fetchSurficialGeology()
    }
  },
  methods: {
    addSurfGeologyLayer (id = 'surficialGeology', data, color = '#00e676') {
      // WIP
      // this.map.addLayer({
      //   id: id,
      //   type: 'line',
      //   source: {
      //     type: 'geojson',
      //     data: data
      //   },
      //   layout: {
      //     visibility: 'visible'
      //   },
      //   paint: {
      //     'line-color': color,
      //     'line-width': 2
      //   }
      // }, 'water_rights_licences')

      // this.map.addLayer({
      //   id: `${id}-labels`,
      //   type: 'symbol',
      //   source: id,
      //   layout: {
      //     'text-field': '{TERRAIN_POLYGON_LBL}',
      //     'text-font': ['BC Sans', 'Arial Unicode MS Bold'],
      //     'text-size': 12
      //   }
      // })
    },
    fetchSurficialGeology () {
      this.surficialGeologyLoading = true
      ApiService.query(`/api/v1/watersheds/${this.watershedID}/surficial_geology`)
        .then(r => {
          this.surficialGeologyByType = r.data.summary_by_type
          console.log('adding data to map')

          this.surficialGeologyByType.forEach((layer, i) => {
            this.addSurfGeologyLayer(`surficialGeology${i}`, this.surficialGeologyByType[i].geojson, '#000')
          })
          this.surficialGeologyLoading = false
        })
        .catch(e => {
          this.surficialGeologyLoading = false
          console.error(e)
        })
    }
  },
  mounted () {
    this.fetchSurficialGeology()
  },
  beforeDestroy () {

  }
}
</script>

<style>

</style>
