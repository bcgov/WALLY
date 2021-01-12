<template>
<div>
  <v-card flat>
    <v-card-text class="pb-0">
      <h3 class="mb-5">Projects</h3>
    </v-card-text>
    <v-card-text v-if="projectsLoading">
      <v-progress-linear show indeterminate></v-progress-linear>
    </v-card-text>
     <!-- <v-treeview
          selected-color="grey darken-2"
          hoverable
          open-on-click
          :items="formattedProjectsData"
        >
        </v-treeview> -->
    <v-card-text v-if="projectsData" class="pt-0">
      <div class="subtitle font-weight-bold">Active Projects List</div>
      <p>
        Project folders that are currently being worked on
      </p>
      <FileBrowser/>

      <v-row>
        <CreateNewProjectModal />
        <!-- <v-file-input
          counter
          multiple
          show-size
          truncate-length="50"
        ></v-file-input> -->
      </v-row>

  <!-- <v-expansion-panels>
    <v-expansion-panel
      v-for="(item) in projectsData"
      :key="item.project_id"
    >
      <v-expansion-panel-header>
        <v-row no-gutters>
            <v-col cols="3">
        {{ item.name }}
            </v-col>
            <v-col cols="4">
        {{ item.description }}
            </v-col>
            <v-col
              cols="4"
              class="text--secondary"
            >
          {{ formatDate(item.create_date) }}
            </v-col>
          </v-row>
      </v-expansion-panel-header>
      <v-expansion-panel-content>
      </v-expansion-panel-content>
    </v-expansion-panel>

  </v-expansion-panels> -->

      <!-- <v-data-table
        :headers="projectsHeaders"
        :items="projectsData"
        :single-expand="singleExpandProjects"
        :expanded.sync="expandedProjects"
        item-key="project_id"
        show-expand
      >
        <template v-slot:[`item.name`]="{ item }">
          {{ item.name }}
        </template>
        <template v-slot:[`item.description`]="{ item }">
          {{ item.description }}
        </template>
        <template v-slot:[`item.create_date`]="{ item }">
          {{ formatDate(item.create_date) }}
        </template>
        <template v-slot:expanded-item="{ headers, item }">
            <DocumentList :project_id="item.project_id"/>
        </template>
      </v-data-table> -->

      <!-- <Upload/> -->

      <!-- <div class="subtitle font-weight-bold">Inactive Projects</div>
      <p>
        Project folders that are no longer in use or have been archived.
      </p>
      <v-data-table
        :headers="projectsHeaders"
        :items="projectsData.filter(p => p.status === 'inactive')"
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
        <template v-slot:[`item.create_date`]="{ item }">
          {{ item.create_date }}
        </template>
      </v-data-table> -->

    </v-card-text>
  </v-card>
</div>
</template>

<script>
import { mapGetters } from 'vuex'
import ApiService from '../../services/ApiService'
// import DocumentList from './DocumentList'
// import Upload from './Upload'
// import SavedAnalysisList from './SavedAnalysisList'
import CreateNewProjectModal from './CreateNewProjectModal'
import FileBrowser from '../filebrowser'
import moment from 'moment'

export default {
  name: 'Projects',
  components: {
    // DocumentList,
    // SavedAnalysisList,
    CreateNewProjectModal,
    // Upload
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
    formattedProjectsData () {
      let projects = this.projectsData.map((pd) => {
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
    ...mapGetters('map', ['isMapReady']),
    fetchProjectsData () {
      this.projectsLoading = true
      moment()
      ApiService.query(`/api/v1/projects/`)
        .then(r => {
          console.log(r.data)
          this.projectsData = r.data
          this.projectsLoading = false
        })
        .catch(e => {
          this.projectsLoading = false
          console.error(e)
        })
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
    },
    formatDate (date) {
      return moment(date).format('MMM DD YYYY')
    }
  },
  watch: {
    isMapReady (value) {
      if (value) {
        this.fetchProjectsData()
      }
    }
  },
  mounted () {
    this.fetchProjectsData()
    if (this.isMapReady()) {
    }
  },
  beforeDestroy () {

  }
}
</script>
