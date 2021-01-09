<template>
  <v-dialog v-model="dialog" width="650">
    <template v-slot:activator="{ on, attrs }">
      <v-col class="text-right">
        <v-btn
          outlined
          color="primary"
          v-bind="attrs"
          v-on="on"
        >
          Upload File
        </v-btn>
      </v-col>
    </template>

    <v-card shaped>
      <v-card-title class="headline grey lighten-3" primary-title>
          Upload File
      </v-card-title>

      <v-card-text class="mt-4">

      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          outlined
          @click="createProject"
          color="primary"
          :disabled="loading"
        >
          <div v-if="!loading">
            Save
          </div>
          <v-progress-circular
            v-if="loading"
            indeterminate
            size=24
            class="ml-1"
            color="primary"
          ></v-progress-circular>
        </v-btn>

      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import ApiService from '../../services/ApiService'

export default {
  name: 'CreateNewProject',
  props: {
    open: Boolean
  },
  data: () => ({
    loading: false,
    dialog: false
  }),
  methods: {
    uploadFile () {
      this.loading = true
      const params = {
        name: this.name,
        description: this.description
      }
      ApiService.post(`/api/v1/projects/`, params)
        .then((res) => {
          // TODO project create logic
          this.dialog = false
          this.loading = false
          console.log(res)
        })
        .catch((error) => {
          this.loading = false
          console.error(error)
        })
    }
  }
}
</script>

<style>
</style>
