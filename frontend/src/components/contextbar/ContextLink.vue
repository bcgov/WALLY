<template>
  <div class="links">
    <div v-for="(item, i) in links" :key="i" min-width="400" class="component">
      <a :href="item" :alt="item.split('/').pop()">{{item.split('/').pop()}}</a>
    </div>
  </div>
</template>
<script>
export default {
  name: 'ContextLink',
  props: {
    data: Object
  },
  data () {
    return {
      links: Array
    }
  },
  mounted () {
    this.links = this.$attrs.links
    // TODO Hack fix on title, add title to link object
  }
}
</script>
