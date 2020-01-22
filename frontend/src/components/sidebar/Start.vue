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
import { mapGetters } from 'vuex'
export default {
  name: 'Start',
  data: () => ({

  }),
  methods: {
    selectPoint () {
      this.draw.changeMode('draw_point')
    }
  },
  computed: {
    ...mapGetters(['draw'])
  }
}
</script>

<style>

</style>
