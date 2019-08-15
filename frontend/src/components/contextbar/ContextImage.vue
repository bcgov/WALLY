
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
  name: 'Image',
  props: {
    source: String
  }
}
</script>
