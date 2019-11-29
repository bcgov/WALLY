<template>
  <h1>{{streams}}</h1>
</template>

<script>
export default {
  name: 'StreamBufferIntersections',
  components: {
  },
  props: ['streamData'],
  data: () => ({
    buffer: 10
  }),
  computed: {
    streams() {
        return this.streamData
    }
  }
}
</script>

<style>

</style>
