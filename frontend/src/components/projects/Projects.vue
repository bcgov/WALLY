<template>
  <v-card flat v-if="this.app.config && this.app.config.projects">
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
      <v-col class="text-right">
        <v-btn
          outlined
          @click="createNewProject"
          color="primary"
        >
          Create New Project
        </v-btn>
      </v-col>
      <v-data-table
        :headers="projectsHeaders"
        :items="projectsData.filter(p => p.status === 'active')"
        :single-expand="singleExpandProjects"
        :expanded.sync="expandedProjects"
        item-key="name"
        show-expand
      >
        <template v-slot:[`item.name`]="{ item }">
          {{ item.name }}
        </template>
        <template v-slot:[`item.description`]="{ item }">
          {{ item.description }}
        </template>
        <template v-slot:[`item.createdAt`]="{ item }">
          {{ item.createdAt }}
        </template>
        <template v-slot:expanded-item="{ headers, item }">
          <td :colspan="headers.length">
            <ProjectDocumentList :project="item.id"/>
            <SavedAnalysisList :project="item.id"/>
          </td>
        </template>
      </v-data-table>

      <div class="subtitle font-weight-bold">Inactive Projects</div>
      <p>
        Project folders that are no longer in use or have been archived.
      </p>
      <v-data-table
        :headers="projectsHeaders"
        :items="projectsData.filter(p => p.status === 'inactive')"
        :single-expand="singleExpandInactiveLicences"
        :expanded.sync="expandedProjects"
        item-key="name"
        show-expand
      >
        <template v-slot:[`item.name`]="{ item }">
          {{ item.name }}
        </template>
        <template v-slot:[`item.description`]="{ item }">
          {{ item.description }}
        </template>
        <template v-slot:[`item.createdAt`]="{ item }">
          {{ item.createdAt }}
        </template>
      </v-data-table>

    </v-card-text>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex'
import ApiService from '../../services/ApiService'
import ProjectDocumentList from './ProjectDocumentList'
import SavedAnalysisList from './SavedAnalysisList'

export default {
  name: 'Projects',
  components: {
    ProjectDocumentList,
    SavedAnalysisList
  },
  props: [''],
  data: () => ({
    projectsLoading: false,
    name: '',
    description: '',
    projectsData: [
      {
        id: '',
        name: 'test',
        description: 'test description',
        createdAt: new Date(),
        status: 'active',
        documents: [
          {
            name: 'test 1',
            url: ''
          }
        ]
      },
      {
        id: '',
        name: 'test',
        description: 'test description',
        createdAt: new Date(),
        status: 'inactive',
        documents: [
          {
            name: 'test 1',
            url: ''
          }
        ]
      }
    ],
    projectsHeaders: [
      { text: 'Name', value: 'name', sortable: true },
      { text: 'Description', value: 'description', align: 'end' },
      { text: 'Create Date', value: 'createdAt', align: 'end' }
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
    ...mapGetters('map', ['map'])
  },
  methods: {
    ...mapGetters('map', ['isMapReady']),
    fetchProjectsData () {
      this.projectsLoading = true
      ApiService.query(`/api/v1/projects/`)
        .then(r => {
          this.projectsData = r.data
          this.projectsLoading = false
        })
        .catch(e => {
          this.projectsLoading = false
          console.error(e)
        })
    },
    toggleCreateProjectModal () {

    },
    createNewProject () {
      const params = {
        name: this.name,
        description: this.description
      }
      ApiService.post(`/api/v1/projects/`, params).then((res) => {
        // TODO project create logic
        console.log(res)
      }).catch((error) => {
        console.error(error)
      })
    }
  },
  watch: {
    isMapReady (value) {
      if (value) {
      }
    }
  },
  mounted () {
    if (this.isMapReady()) {
    }
  },
  beforeDestroy () {

  }
}
</script>
