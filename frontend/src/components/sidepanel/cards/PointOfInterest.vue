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
    <v-row class="pa-5">
      <v-col cols=12 lg=8>
        <p>Select a point on the map.</p>
      </v-col>
      <v-col class="text-right">
        <v-btn @click="selectPoint" color="primary" outlined>Draw point</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'PlacePointOfInterest',
  components: {
  },
  data: () => ({

  }),
  methods: {
    selectPoint () {
      if (this.draw && this.draw.changeMode) {
        this.draw.changeMode('draw_point')
      }
    }
  },
  computed: {
    ...mapGetters('map', ['draw']),
    ...mapGetters(['dataMartFeatureInfo'])
  },
  mounted () {
    this.selectPoint()
  },
  beforeDestroy () {
    this.draw.changeMode('simple_select')
    // this.$store.dispatch('map/clearSelections')
  }
}
</script>

<style>

</style>
