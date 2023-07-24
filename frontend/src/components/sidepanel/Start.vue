<template>
  <v-container>
    <v-row>
      <v-col>
        <v-btn color="secondary" @click="selectPointOfInterest">Place a point of interest</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions } from 'vuex'
export default {
  name: 'Start',
  data: () => ({

  }),
  methods: {
    ...mapActions('map', ['setDrawMode', 'selectPointOfInterest'])
  }
}
</script>

<style>

</style>
