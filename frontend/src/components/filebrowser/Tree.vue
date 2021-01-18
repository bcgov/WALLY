<template>
    <v-card flat tile width="250" min-height="380" class="d-flex flex-column folders-tree-card">
        <div class="grow scroll-x">
            <v-treeview
                :open="open"
                :active="active"
                :items="projectList"
                :search="filter"
                v-on:update:active="activeChanged"
                item-key="id"
                item-text="name"
                dense
                activatable
                transition
                class="folders-tree"
            >
                <template v-slot:prepend="{ item, open }">
                    <v-icon
                        v-if="item.type === 'root' || item.type === 'dir'"
                    >
                      {{ open ? 'mdi-folder-open-outline' : 'mdi-folder-outline' }}
                    </v-icon>
                    <span
                      v-if="item.type === 'root' || item.type === 'dir'"
                      class='ml-3'
                    >
                      {{item.name}}
                    </span>
                    <span v-else>{{item.filename}}</span>
                    <!-- <v-icon v-else>{{ icons[item.extension.toLowerCase()] || icons['other'] }}</v-icon> -->
                </template>
                <template v-slot:label="{ item }">
                  <span></span>
                    <!-- <v-btn
                        icon
                        v-if="item.type === 'root' || item.type === 'dir'"
                        @click.stop="item.type === 'root' ? readFolder(item) : fetchProjectDocuments(item)"
                        class="ml-1"
                    >
                        <v-icon class="pa-0 mdi-18px" color="grey lighten-1">mdi-refresh</v-icon>
                    </v-btn> -->
                </template>
            </v-treeview>
        </div>
        <v-divider></v-divider>
        <v-toolbar dense flat class="shrink">
            <v-text-field
                solo
                flat
                hide-details
                label="Filter"
                v-model="filter"
                prepend-inner-icon="mdi-filter-outline"
                class="ml-n3"
            ></v-text-field>
            <v-tooltip top>
                <template v-slot:activator="{ on }">
                    <v-btn icon @click="init" v-on="on">
                        <v-icon>mdi-collapse-all-outline</v-icon>
                    </v-btn>
                </template>
                <span>Collapse All</span>
            </v-tooltip>
        </v-toolbar>
    </v-card>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from 'vuex'
import ApiService from '../../services/ApiService'

export default {
  props: {
    icons: Object,
    endpoints: Object,
    refreshPending: Boolean
  },
  data () {
    return {
      open: [],
      active: [],
      filter: ''
    }
  },
  computed: {
    ...mapGetters(['selectedProjectItem', 'projects']),
    projectList () {
      let projectList = [{
        type: 'root',
        extension: '',
        name: 'My Projects'
      }]
      projectList[0].children = this.projects.map(p => {
        p.type = 'dir'
        // p.project_id = p.project_id.toString()
        return p
      })
      return projectList
    }
  },
  methods: {
    ...mapActions(['getProjects']),
    ...mapMutations(['setSelectedProjectItem', 'setActiveFiles']),
    init () {
      this.open = []
      this.getProjects()
    },
    async fetchProjectDocuments (item) {
      if (!item) { return }

      console.log('fetchProjectDocuments start', item)

      this.$emit('loading', true)
      let url = this.endpoints.documents.url
        .replace(new RegExp('{projectId}', 'g'), item.project_id)

      let response = await ApiService.query(url)
      this.setActiveFiles(response.data)
      item.children = response.data

      console.log('fetched project documents', response.data)
      this.$emit('loading', false)
    },
    activeChanged (active) {
      if (!active[0]) { return }
      let split = active[0].split('-')
      const type = split[0]
      const id = split[1]
      if (type === 'project') {
        const project = this.findChildProject(id)
        this.fetchProjectDocuments(project)
        this.setSelectedProjectItem(project)
      } else if (type === 'document') {
        // TODO what happens when a document
        // is clicked in the tree, show more info?
      }
    },
    findChildProject (projectId) {
      const children = this.projectList[0].children
      return children.find((x) => x.project_id.toString() === projectId)
    }
  },
  watch: {
    projects () {
    }
  },
  created () {
    this.init()
  }
}
</script>

<style lang="scss" scoped>
.folders-tree-card {
    height: 100%;

    .scroll-x {
        overflow-x: auto;
    }

    ::v-deep .folders-tree {
        width: fit-content;
        min-width: 250px;

        .v-treeview-node {
            cursor: pointer;

            &:hover {
                background-color: rgba(0, 0, 0, 0.02);
            }
        }
    }
}
</style>
