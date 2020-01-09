<template>
  <v-container class="pt-5">
    <v-toolbar flat>
      <v-banner color="indigo"
                icon="mdi-vector-line"
                icon-color="white"
                width="100%"
      >
        <v-toolbar-title>
          Cross section
        </v-toolbar-title>
      </v-banner>
    </v-toolbar>
    <div class="pa-5">
      <p>Draw a line to plot a cross section of subsurface data.</p>
    </div>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'DrawCrossSection',
  data: () => ({

  }),
  methods: {
    drawLine () {
      this.draw.changeMode('draw_line_string')
    }
  },
  computed: {
    ...mapGetters(['draw'])
  },
  mounted () {
    this.drawLine()
  },
  beforeDestroy () {
    this.draw.changeMode('simple_select')
  }
}
</script>

<style>

</style>
