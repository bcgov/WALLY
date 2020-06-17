<template>
  <v-dialog v-if="name" width="650">
    <template v-slot:activator="{ on }">
      <v-icon class="float-right" v-on="on">
        mdi-information-outline
      </v-icon>
    </template>
    <v-card shaped>
      <v-card-title class="headline grey lighten-3" primary-title>
        <v-icon class="mr-2">
          mdi-information-outline
        </v-icon>
        <div style="{color:grey}">{{name}}</div>
      </v-card-title>
      <v-card-text class="mt-4">
        {{description}}
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions v-if="url">
        <v-spacer></v-spacer>
        <v-btn
          text
          color="primary accent-4"
          v-bind:href=url
          target="_blank"
        >
          Link to Data Source
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'Dialog',
  props: {
    name: String,
    description: String,
    url: String
  }
}
</script>

<style>
</style>
