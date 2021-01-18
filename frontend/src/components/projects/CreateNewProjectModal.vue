<template>
  <v-dialog v-model="dialog" width="650">
    <template v-slot:activator="{ on, attrs }">
        <v-btn
          outlined
          color="primary"
          v-bind="attrs"
          v-on="on"
          class='mb-2 p-3'
        >
          <v-icon class='mr-1'>mdi-folder-plus-outline</v-icon>
          Create Project
        </v-btn>
    </template>

    <v-card shaped>
      <v-card-title class="headline grey lighten-3" primary-title>
          Create Project
      </v-card-title>
      <v-card-text class="mt-4">
        <v-row>
          <v-col cols="12" md="12" align-self="center">
            <v-text-field
              label="Project Name"
              placeholder="Enter an application # or area name"
              v-model="name"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="12">
            <v-text-field
              label="Project Description"
              placeholder="Enter a description of the work to be done"
              v-model="description"
            ></v-text-field>
          </v-col>
        </v-row>
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
import { mapActions } from 'vuex'
import ApiService from '../../services/ApiService'

export default {
  name: 'CreateNewProject',
  props: {
    open: Boolean
  },
  data: () => ({
    loading: false,
    dialog: false,
    name: '',
    description: ''
  }),
  methods: {
    ...mapActions(['getProjects']),
    createProject () {
      if (this.name.length < 3) {
        // TODO add user notify that at least 3 characters
        // are needed for a project name
        return
      }
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
          this.getProjects()
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
