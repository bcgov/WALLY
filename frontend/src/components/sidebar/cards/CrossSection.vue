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
    <WellsCrossSection
      :record="dataMartFeatureInfo"
      :coordinates="dataMartFeatureInfo.geometry.coordinates"
      v-if="dataMartFeatureInfo && dataMartFeatureInfo.display_data_name === 'user_defined_line'"/>
    <div class="pa-5" v-else>
      <p>Draw a line to plot a cross section of subsurface data.</p>
    </div>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'

import WellsCrossSection from '../../analysis/WellsCrossSection'

export default {
  name: 'DrawCrossSection',
  components: {
    WellsCrossSection
  },
  data: () => ({

  }),
  methods: {
    drawLine () {
      if (!this.draw || (this.dataMartFeatureInfo && this.dataMartFeatureInfo.display_data_name === 'user_defined_line')) {
        return
      }
      this.draw.changeMode('draw_line_string')
    }
  },
  computed: {
    ...mapGetters(['draw', 'dataMartFeatureInfo'])
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
