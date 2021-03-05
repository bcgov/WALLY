<template>
    <v-card flat tile width="250" min-height="380" class="d-flex flex-column folders-tree-card">
        <div class="grow scroll-x">
            <v-treeview
                :open="open"
                :active="active"
                :items="projectTree"
                :search="filter"
                v-on:update:active="selectProject"
                v-on:update:open="toggleProjectsFolder"
                item-key="id"
                item-text="name"
                dense
                activatable
                transition
                class="folders-tree"
                open-on-click
            >
                <template v-slot:prepend="{ item, open }">
                    <span class="mr-2">{{item.fileCount}}</span>
                    <v-icon
                        v-if="item.type === 'root' || item.type === 'dir'"
                    >
                      {{ open ? 'mdi-folder-open-outline' : 'mdi-folder-outline' }}
                    </v-icon>
                    <span
                      v-if="item.type === 'root' || item.type === 'dir'"
                      class='ml-1 overflow-hidden'
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

export default {
  props: {
    icons: Object,
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
    ...mapGetters(['selectedProject', 'projectsList']),
    projectTree () {
      let tree = [{
        type: 'root',
        extension: '',
        name: 'My Projects'
      }]
      if (this.projectsList.length > 0) {
        tree[0].children = this.projectsList.map(p => {
          return {
            id: p.project_uuid,
            project_uuid: p.project_uuid,
            description: p.description,
            name: p.name,
            type: 'dir',
            fileCount: p.children.length,
            children: [] // stops documents from showing in the left side tree view
          }
        })
      }
      return tree
    }
  },
  methods: {
    ...mapActions(['getProjects', 'getProjectFiles', 'deselectProjects']),
    ...mapMutations(['setSelectedProject', 'setProjectFiles']),
    init () {
      this.open = []
      this.getProjects()
    },
    selectProject (tree) {
      if (!tree[0]) {
        this.deselectProjects()
        return
      }
      let uuid = tree[0]
      const project = this.projectsList.find((p) => p.project_uuid === uuid)
      this.setSelectedProject(project)
    },
    toggleProjectsFolder () {
      this.active = []
      this.deselectProjects()
    }
  },
  watch: {
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
        overflow-x: hidden;
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
