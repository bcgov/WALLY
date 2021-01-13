<template>
    <v-toolbar flat dense color="blue-grey lighten-5">
        <v-toolbar-items>
          <create-new-project-modal />
        </v-toolbar-items>
        <div class="flex-grow-1"></div>
        <template v-if="$vuetify.breakpoint.smAndUp">
          <span>{{selectedName}}</span>
          <v-btn icon @click="$refs.inputUpload.click()" title="Upload Files">
            <v-icon>mdi-plus-circle</v-icon>
            <input v-show="false" ref="inputUpload" type="file" multiple @change="addFiles" />
          </v-btn>
        </template>
    </v-toolbar>
</template>

<script>
import { mapGetters } from 'vuex'
import CreateNewProjectModal from '../projects/CreateNewProjectModal.vue'
export default {
  components: { CreateNewProjectModal },
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

    async addFiles (event) {
      this.$emit('add-files', event.target.files)
      this.$refs.inputUpload.value = ''
    }
  }
}
</script>

<style>
</style>
