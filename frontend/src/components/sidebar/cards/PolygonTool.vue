<template>
  <v-container class="pt-5">
    <v-toolbar flat>
      <v-banner color="indigo"
                icon="mdi-shape-polygon-plus"
                icon-color="white"
                width="100%"
      >
        <v-toolbar-title>
          Polygon selection
        </v-toolbar-title>
      </v-banner>
    </v-toolbar>
    <div class="pa-5">
      <p>Start drawing a polygon to select data in a region.</p>
      <p>Click on any point a second time to complete the polygon.</p>
    </div>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'DrawPolygon',
  data: () => ({

  }),
  methods: {
    selectPoint () {
      this.draw.changeMode('draw_polygon')
    }
  },
  computed: {
    ...mapGetters('map', ['draw'])
  },
  mounted () {
    this.selectPoint()
  },
  beforeDestroy () {
    this.draw.changeMode('simple_select')
  }
}
</script>

<style>

</style>
