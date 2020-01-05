<template>
  <v-container class="pt-5">
    <v-toolbar flat>
      <v-banner color="indigo"
                icon="mdi-map-marker"
                icon-color="white"
                width="100%"
      >
        <v-toolbar-title>
          Point of interest
        </v-toolbar-title>
      </v-banner>
    </v-toolbar>
    <div class="pa-5">
      <p>Select a point on the map.</p>
    </div>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'PlacePointOfInterest',
  data: () => ({

  }),
  methods: {
    selectPoint () {
      this.draw.changeMode('draw_point')
    }
  },
  computed: {
    ...mapGetters(['draw'])
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
