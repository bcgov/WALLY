<template>
  <v-card flat v-if="stations">
    <p class="title font-weight-bold">Hydrometric Stations</p>
    <v-expansion-panels accordion multiple hover flat>
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
      console.log(newValue, oldValue)
    }
  },
  mounted () {

  }
}
</script>
