
<template>
<div>
  <v-img
    :src=source
    aspect-ratio="2.75"
  ></v-img>
</div>
</template>
<script>
export default {
  name: 'ContextImage',
  props: {
    source: String
  }
}
</script>
