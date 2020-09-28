<template>
  <v-card flat v-if="this.surface_water_design_v2">
    <v-card-title
      class="title mt-5 ml-3 mr-3 pa-1 mb-2"
      dark>
      Hydrometric Stations
    </v-card-title>
    <v-card-text v-if="stations && stations.length > 0">
      <v-expansion-panels accordion multiple hover flat
                          v-if="stations && stations.length > 0">
        <v-expansion-panel v-for="(item, i) in stations" v-bind:key="i">
          <v-expansion-panel-header :key="i">
            {{item.properties.name}}
            ({{item.id}})
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <FeatureStreamStation :record="item" />
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card-text>
    <v-card-text v-else>
      <p class="text--disabled">No hydrometric stream flow stations found in this area</p>
    </v-card-text>
  </v-card>
  <v-card flat v-else>
    <p class="title font-weight-bold">Hydrometric Stations</p>
    <v-expansion-panels accordion multiple hover flat
                        v-if="stations && stations.length > 0">
      <v-expansion-panel v-for="(item, i) in stations" v-bind:key="i">
        <v-expansion-panel-header :key="i">
          {{item.properties.name}}
          ({{item.id}})
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <FeatureStreamStation :record="item" />
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
    <p v-else class="text--disabled">No hydrometric stream flow stations found in this area</p>
  </v-card>
</template>
<script>
import FeatureStreamStation from '../../../features/FeatureStreamStation'

export default {
  name: 'HydrometricStationsContainer',
  components: {
    FeatureStreamStation
  },
  props: ['stations', 'surface_water_design_v2'],
  data: () => ({
  }),
  watch: {
    stations (newValue, oldValue) {
    }
  },
  mounted () {

  }
}
</script>
