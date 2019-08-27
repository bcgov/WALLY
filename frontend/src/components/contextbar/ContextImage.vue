
<template>
<div>
  <img :src="source" alt="Image" />
</div>
</template>
<script>
/* WARNING: We use img because the v-img tag uses  */
/* background-image which isn't good for SEO and accessibility */
export default {
  name: 'ContextImage',
  props: {
    source: String
  }
}
</script>
<style>
  div[type=image] {
  overflow: hidden
  }
</style>
