<template>
  <div class="links">
    <h1 style="margin-bottom: 5px">
      {{this.title}}
    </h1>
    <v-card v-for="(item, i) in links" :key="i" min-width="400" class="component">
      <v-card-title>
        <span v-if="item && item">Link to Source: <a :href="item.link" :alt="item.label">{{item.label}}</a></span>
      </v-card-title>
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
      links: Array
    }
  },
  mounted () {
    this.links = this.$attrs.links
    this.title = this.$attrs.title
  }
}
</script>
