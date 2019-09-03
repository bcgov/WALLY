<template>
  <a :href="source" :alt="title">{{title}}</a>
</template>
<script>
export default {
  name: 'ContextLink',
  props: {
    source: String,
    data: Object,
    title: String
  },
  mounted () {
    this.source = this.$attrs.link
    // TODO Hack fix to demo for review, add title to link object
    this.title = this.$attrs.link.split('/').pop()
  }
}
</script>
