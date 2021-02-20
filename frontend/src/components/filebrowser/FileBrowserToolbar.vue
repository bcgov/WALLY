<template>
    <v-toolbar flat dense color="blue-grey lighten-5">
        <FileBrowserConfirmDialog ref="confirmDeleteProject"></FileBrowserConfirmDialog>
        <v-toolbar-items>
          <ProjectCreateModal/>
        </v-toolbar-items>
        <div class="flex-grow-1"></div>
        <template v-if="selectedName">
          <span><b>Project: </b> {{selectedName}}</span>
          <v-btn icon @click="$refs.inputUpload.click()" title="Upload Files">
            <v-icon>mdi-plus-circle</v-icon>
            <input v-show="false" ref="inputUpload" type="file" multiple @change="addFiles" />
          </v-btn>
          <v-btn icon @click="downloadProject" title="Download Project">
            <v-icon>mdi-download</v-icon>
          </v-btn>
          <v-btn icon @click="promptDelete" title="Delete Project">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>
    </v-toolbar>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import FileBrowserConfirmDialog from './FileBrowserConfirmDialog.vue'
import ProjectCreateModal from '../projects/ProjectCreateModal.vue'
export default {
  components: {
    FileBrowserConfirmDialog,
    ProjectCreateModal
  },
  props: {
  },
  data () {
    return {
    }
  },
  computed: {
    ...mapGetters(['selectedProject']),
    selectedName () {
      let name = this.selectedProject?.name
      let filename = this.selectedProject?.filename
      if (name) {
        return name
      } else if (filename) {
        return filename
      } else {
        return ''
      }
    }
  },
  methods: {
    ...mapActions(['deleteProject', 'downloadProject']),
    async addFiles (event) {
      this.$emit('add-files', event.target.files)
      this.$refs.inputUpload.value = ''
    },
    async promptDelete () {
      const name = this.selectedProject?.name
      // eslint-disable-next-line
      const projectId = this.selectedProject?.project_id
      console.log(projectId)
      if (projectId) {
        let confirmed = await this.$refs.confirmDeleteProject.open(
          'Delete',
          `Are you sure<br>you want to delete <br><b>Project: </b><em>${name}</em>`
        )
        if (confirmed) {
          this.deleteProject(projectId)
        }
      }
    }

  }
}
</script>

<style>
</style>
