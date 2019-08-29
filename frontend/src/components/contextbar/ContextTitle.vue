<template>
  <h1>{{title}}</h1>
</template>
<script>
export default {
  name: 'ContextTitle',
  props: {
    data: Object,
    chartKey: Number
  },
  data () {
    return {
      title: ''
    }
  },
  mounted () {
    this.title = this.data
  }
}
</script>
