<template>
  <v-card flat>
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
  props: ['stations'],
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
