<template>
  <div class="links">
    <h1 class="mb-4">
      {{this.title}}
    </h1>
    <v-card v-for="(item, i) in links" :key="i" min-width="400" class="component">
      <v-card-text>
        <span v-if="item && item.link && item.label"><a :href="item.link" :alt="item.label" target="_blank">{{item.label}}</a></span>
        <span v-else-if="!item.label || item.label==''"><a :href="item.link" :alt="item.link" target="_blank">{{item.link}}</a></span>
      </v-card-text>
    </v-card>
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
      links: Array,
      title: String
    }
  },
  mounted () {
    this.links = this.$attrs.links
    this.title = this.$attrs.title
  }
}
</script>