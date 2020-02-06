<template>
  <v-container>
    <v-row>
      <v-col>
        <v-btn color="secondary" @click="selectPoint">Place a point of interest</v-btn>
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
    selectPoint () {
      this.setDrawMode('draw_point')
    },
    ...mapActions('map', ['setDrawMode'])
  }
}
</script>

<style>

</style>
