<template>
  <div>
    <div class="title my-5">Watershed Details</div>
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
  },
  methods: {
  },
  mounted () {
  }
}
</script>

<style>

</style>
