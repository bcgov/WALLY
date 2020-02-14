<template>
  <div>
    <div class="title my-5">Watershed Details</div>
      <div class="my-3" v-if="watershedArea">
        <span class="font-weight-bold">Area:</span>
        {{watershedArea.toFixed(1) }} sq. m ({{ (watershedArea / 1e6).toFixed(2)}} sq. km) </div>
    <SurficialGeology :watershedID="watershedID" :record="record"/>
  </div>
</template>

<script>
import SurficialGeology from './SurficialGeology'

export default {
  name: 'WatershedDetails',
  props: ['watershedID', 'record'],
  components: {
    SurficialGeology
  },
  data: () => ({
  }),
  watch: {
  },
  computed: {
    watershedArea () {
      if (!this.record || !this.record.properties['area']) {
        return null
      }

      return Number(this.record.properties['area'])
    }
  },
  methods: {
  },
  mounted () {
  }
}
</script>

<style>

</style>
