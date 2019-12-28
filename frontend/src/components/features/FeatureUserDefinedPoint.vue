<template>
  <v-sheet class="pt-5">
    <v-toolbar flat>
      <v-banner color="indigo"
                icon="mdi-map-marker"
                icon-color="white"
                width="100%"
      >
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
  }
}
</script>

<style>

</style>
