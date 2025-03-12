<template>
<div>
  <v-card flat>
    <v-card-text class="pb-0">
      <h3 class="mb-5">Projects</h3>
    </v-card-text>
    <v-card-text v-if="projectsLoading">
      <v-progress-linear show indeterminate></v-progress-linear>
    </v-card-text>
    <v-card-text v-if="projectsData" class="pt-0">
      <div class="subtitle font-weight-bold">Active Projects List</div>
      <p>
        Project folders that are currently being worked on
      </p>
      <FileBrowser/>
    </v-card-text>
  </v-card>
</div>
</template>

<script>
import { mapGetters } from 'vuex'
import FileBrowser from '../filebrowser/FileBrowser'

export default {
  name: 'ProjectList',
  components: {
    FileBrowser
  },
  props: [''],
  data: () => ({
    projectsLoading: false,
    name: '',
    description: '',
    projectsData: [],
    projectsHeaders: [
      { text: 'Project Name', value: 'name', sortable: true },
      { text: 'Project Description', value: 'description', align: 'end' },
      { text: 'Create Date', value: 'create_date', align: 'end' }
    ],
    projectStatus: [
      'active',
      'inactive',
      'archived'
    ],
    singleExpandProjects: false,
    expandedProjects: [],
    featureDescription: {

    }
  }),
  computed: {
    ...mapGetters('map', ['map']),
    ...mapGetters(['app']),
    formattedProjectsData () {
      const projects = this.projectsData.map((pd) => {
        return {
          ...pd,
          children: [{
            id: 1,
            name: 1
          },
          {
            id: 2,
            name: 2
          }]
        }
      })
      console.log(projects)
      return projects
    }
  },
  methods: {
    ...mapGetters('map', ['isMapReady'])
  }
}
</script>
