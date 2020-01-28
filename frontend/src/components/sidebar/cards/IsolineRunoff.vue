<template>
  <v-container class="pt-5">
    <v-toolbar flat>
      <v-banner color="indigo"
                icon="mdi-vector-line"
                icon-color="white"
                width="100%"
      >
        <v-toolbar-title>
          Isoline Annual Runoff Analysis
        </v-toolbar-title>
      </v-banner>
    </v-toolbar>
    <div
    v-if="dataMartFeatureInfo && dataMartFeatureInfo.display_data_name === 'point_of_interest'">
    </div>

    <v-row class="pa-5" v-else>
      <v-col cols=12 lg=8>
        <p>Select an area of interest.</p>
      </v-col>
      <v-col class="text-right">
        <v-btn @click="selectArea" color="primary" outlined>Draw Polygon</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'IsolineRunoff',
  components: {
  },
  data: () => ({
  }),
  methods: {
    selectArea () {
      if (this.draw && this.draw.changeMode) {
        this.draw.changeMode('draw_polygon')
      }
    }
  },
  computed: {
    ...mapGetters(['draw', 'dataMartFeatureInfo', 'isMapLayerActive'])
  },
  mounted () {
    this.selectArea()
  },
  beforeDestroy () {
    this.draw.changeMode('simple_select')
  }
}
</script>

<style>
</style>