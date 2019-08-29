<template>
    <a :href="source" :alt="title">{{title}}</a>
</template>
<script>
export default {
  name: 'ContextLink',
  props: {
    source: String,
    title: String
  }
}
</script>
