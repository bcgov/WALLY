<template>
  <v-card elevation=0>
    <v-card-text>
      <div class="grey--text text--darken-4 headline" id="communityName">{{ record.properties.FIRST_NATION_BC_NAME }}</div>
      <div class="grey--text text--darken-2 title">First Nations Community Locations</div>
      <v-divider></v-divider>
      <v-list dense class="mx-0 px-0">
        <v-list-item class="feature-content">
          <v-list-item-content>First Nation Name (BC)</v-list-item-content>
          <v-list-item-content>{{record.properties.FIRST_NATION_BC_NAME}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>URL</v-list-item-content>
          <v-list-item-content>
            <a :href="record.properties.URL_TO_BC_WEBSITE" target="_blank">
            {{record.properties.URL_TO_BC_WEBSITE}}
            </a>
          </v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Preferred name</v-list-item-content>
          <v-list-item-content>{{record.properties.PREFERRED_NAME}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Language group</v-list-item-content>
          <v-list-item-content>{{record.properties.LANGUAGE_GROUP}}</v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'FeatureCommunityLocation',
  props: {
    record: Object
  },
  data () {
    return {}
  },
  methods: {}
}
</script>

<style>

</style>
