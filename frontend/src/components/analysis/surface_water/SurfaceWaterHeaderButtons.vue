<template>
  <v-row>
    <v-col>
      <v-card-text v-for="layer in layerSelection" :key="layer.name">
        test
        {{layer.name}}
      </v-card-text>
      <v-btn-toggle>
        <v-menu offset-y
                :close-on-content-click="false">
          <template v-slot:activator="{ on, attrs }">
            <v-btn outlined small
                   color="primary" class=""
                   v-bind="attrs"
                   v-on="on">
            <span class="hidden-sm-and-down">
            See on map
            </span>
            </v-btn>
            <v-btn
              small
              icon
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>layers</v-icon>
            </v-btn>
          </template>
          <v-card class="pa-5">
            <v-checkbox small class="mt-0"
                        v-for="(layer, id) in layerSelection" :label="layer.name" :key="id"
                        v-model="layers[id]"
                        @click="handleSelectLayer(id)"
            />
          </v-card>
        </v-menu>

      </v-btn-toggle>
    </v-col>
    <v-col>
    </v-col>
    <v-col class="text-right">
      <v-btn-toggle>

        <v-menu open-on-hover offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-btn outlined small
                   color="blue" class=""
                   v-bind="attrs"
                   v-on="on"
            >
            <span class="hidden-sm-and-down">
            Export
            </span>
            </v-btn>
            <v-btn
              small
              dark
              icon
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>expand_more</v-icon>
            </v-btn>
          </template>
          <v-list >
            <v-list-item @click="exportPDF" disabled>
              <v-list-item-title>
                <v-icon class="mr-1">cloud_download</v-icon>
                PDF
              </v-list-item-title>
            </v-list-item>
            <v-list-item @click="exportExcel">
              <v-list-item-title >
                <v-icon class="mr-1">cloud_download</v-icon>
                Excel
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>

      </v-btn-toggle>
      <v-btn outlined small color="primary" class="ml-1"
             @click="resetWatershed">
        <v-icon small>refresh</v-icon>
        Reset
      </v-btn>
    </v-col>
  </v-row>
</template>
<script>
import EventBus from '../../../services/EventBus'

export default {
  name: 'SurfaceWaterHeaderButtons',
  props: ['layers'],
  data: () => ({
    // layers: this.layers
    layerSelection: {}
  }),
  methods: {
    handleSelectLayer (layerID) {
      console.log(layerID, 'selected', this.layers[layerID])
      if (this.layers[layerID].active) {
        this.$store.dispatch('map/removeMapLayer', layerID)
        this.layers[layerID].active = false
      } else {
        this.$store.dispatch('map/addMapLayer', layerID)
        this.layers[layerID].active = true
      }
    },
    resetWatershed () {
      EventBus.$emit('watershed:reset')
    },
    exportPDF () {
      console.log('calling?')
      EventBus.$emit('watershed:export:pdf')
    },
    exportExcel () {
      EventBus.$emit('watershed:export:excel')
    }
  },
  mounted () {
    Object.keys(this.layers).forEach((layerID) => {
      this.layerSelection[layerID] = {
        name: this.layers[layerID],
        active: true
      }
      // console.log(this.layerSelection[layerID])
    })
    console.log(this.layerSelection)
  }
}
</script>
