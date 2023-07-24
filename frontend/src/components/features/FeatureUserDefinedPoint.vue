<template>
  <v-sheet class="pt-5">
    <v-toolbar flat>
      <v-banner width="100%">
        <v-avatar slot="icon" color="indigo">
          <v-icon
            icon="mdi-map-marker"
            color="white">
            mdi-map-marker
          </v-icon>
        </v-avatar>
        <v-toolbar-title>
          Point of interest
        </v-toolbar-title>
        {{coordinates}}
      </v-banner>
    </v-toolbar>
  </v-sheet>
</template>

<script>
export default {
  name: 'FeatureUserDefined',
  components: {

  },
  props: ['record'],
  data: () => ({
    radius: 1000
  }),
  computed: {
    coordinates () {
      return this.record.geometry.coordinates.map((x) => {
        return x.toFixed(5)
      }).join(', ')
    }
  },
  beforeDestroy () {
    this.$store.dispatch('map/clearSelections')
  }
}
</script>

<style>

</style>
