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
          Upload File To Project
        </v-btn>
    </template>

    <v-card shaped>
      <v-card-title class="headline grey lighten-3" primary-title>
          Select a Project
      </v-card-title>
      <v-select
        solo
        :items="projects"
        placeholder="Select a Project"
        v-model="selectedProject"
      />

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
import { mapGetters } from 'vuex'

export default {
  name: 'ProjectFileUpload',
  props: {
    open: Boolean,
    selectedProject: {}
  },
  data: () => ({
  }),
  methods: {
  },
  computed: {
    ...mapGetters(['projects']),
    projects () {
      return this.projects.map(project => {
        return { value: project.project_uuid, text: project.name }
      })
    }
  }
}
</script>

<style>
</style>
