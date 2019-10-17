<template>
  <v-card elevation=0>
    <v-card-text>
      <div class="grey--text text--darken-4 headline" id="aquiferTitle">{{ record.properties.TITLE }}</div>
      <div class="grey--text text--darken-2 title">Ecological Reports Catalogue</div>
      <v-divider></v-divider>
      <dl class="grey--text text--darken-4">
        <dt>Short description:</dt>
        <dd>{{record.properties.SHORT_DESCRIPTION}}</dd>

        <dt>Author:</dt>
        <dd>{{record.properties.AUTHOR}}</dd>

        <dt>Date published:</dt>
        <dd>{{record.properties.DATE_PUBLISHED}}</dd>

        <dt>Available at:</dt>
        <dd><a :href="link" target="_blank">{{link}}</a></dd>
      </dl>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'FeatureAquifer',
  props: {
    record: Object
  },
  data () {
    return {
    }
  },
  computed: {
    id () {
      return this.record.properties.REPORT_ID
    },
    link () {
      return `https://a100.gov.bc.ca/pub/acat/public/viewReport.do?reportId=${this.id}`
    }
  },
  methods: {
  }
}
</script>

<style>

</style>
