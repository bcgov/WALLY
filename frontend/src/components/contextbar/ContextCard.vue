<template>
<div>
  <v-card-title primary-title>
    <div>
      <h3 class="headline mb-0 title">{{title}}</h3>
      <div class="description">
        {{description}}
      </div>
    </div>
  </v-card-title>
</div>
</template>
<script>
export default {
  name: 'ContextCard',
  props: {
    title: String,
    description: String
  }
}
</script>
