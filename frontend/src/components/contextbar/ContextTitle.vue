<template>
  <div :key="chartKey">
    <div style="text-align: center; margin: 15px;"><b>{{title}}</b></div>
  </div>
</template>

<script>
    export default {
      name: "ContextTitle",
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
