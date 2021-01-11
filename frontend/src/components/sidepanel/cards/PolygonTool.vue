<template>
  <v-container class="pt-5">
    <v-toolbar flat>
      <v-banner width="100%">
        <v-avatar slot="icon" color="indigo">
          <v-icon
            icon="mdi-shape-polygon-plus"
            color="white">
            mdi-shape-polygon-plus
          </v-icon>
        </v-avatar>
        <v-toolbar-title>
          Polygon selection
        </v-toolbar-title>
      </v-banner>
    </v-toolbar>
    <v-row class="pa-5">
      <v-col cols=12 lg=8>
        <p>Zoom into an area of interest on the map and start drawing a polygon to select data in that region. Click on any point a second time to complete the polygon.</p>
      </v-col>
      <v-col class="text-right">
        <v-btn @click="selectPoint" color="primary" outlined :disabled="buttonClicked">Draw polygon</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
export default {
  name: 'DrawPolygon',
  data: () => ({
    buttonClicked: false
  }),
  methods: {
    selectPoint () {
      this.setDrawMode('draw_polygon')
      this.buttonClicked = true
    },
    ...mapActions('map', ['setDrawMode'])
  },
  computed: {
    ...mapGetters('map', ['draw']),
    ...mapGetters(['dataMartFeatures'])
  },
  watch: {
    dataMartFeatures (value) {
      if (value && value.length > 0) {
        this.$router.push({ name: 'multiple-features' })
      }
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
