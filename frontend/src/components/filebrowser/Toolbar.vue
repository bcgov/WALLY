<template>
    <v-toolbar flat dense color="blue-grey lighten-5">
        <confirm ref="confirmDeleteProject"></confirm>
        <v-toolbar-items>
          <create-new-project-modal />
        </v-toolbar-items>
        <div class="flex-grow-1"></div>
        <template v-if="selectedName">
          <span><b>Project: </b> {{selectedName}}</span>
          <v-btn icon @click="$refs.inputUpload.click()" title="Upload Files">
            <v-icon>mdi-plus-circle</v-icon>
            <input v-show="false" ref="inputUpload" type="file" multiple @change="addFiles" />
          </v-btn>
          <v-btn icon @click="promptDelete" title="Upload Files">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>
    </v-toolbar>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import CreateNewProjectModal from '../projects/CreateNewProjectModal.vue'
import Confirm from './Confirm.vue'
export default {
  components: { CreateNewProjectModal, Confirm },
  props: {
  },
  data () {
    return {
    }
  },
  computed: {
    ...mapGetters(['selectedProjectItem']),
    selectedName () {
      let name = this.selectedProjectItem?.name
      let filename = this.selectedProjectItem?.filename
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
    ...mapActions(['deleteProject']),
    async addFiles (event) {
      this.$emit('add-files', event.target.files)
      this.$refs.inputUpload.value = ''
    },
    async promptDelete () {
      const name = this.selectedProjectItem?.name
      // eslint-disable-next-line
      const projectId = this.selectedProjectItem?.project_id
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
