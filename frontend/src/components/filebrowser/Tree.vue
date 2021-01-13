<template>
    <v-card flat tile width="250" min-height="380" class="d-flex flex-column folders-tree-card">
        <div class="grow scroll-x">
            <v-treeview
                :open="open"
                :active="active"
                :items="items"
                :search="filter"
                v-on:update:active="activeChanged"
                item-key="project_id"
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
import { mapGetters, mapMutations } from 'vuex'
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
      items: [],
      filter: ''
    }
  },
  computed: {
    ...mapGetters(['selectedProjectItem'])
  },
  methods: {
    ...mapMutations(['setSelectedProjectItem', 'setActiveFiles']),
    init () {
      this.open = []
      this.items = []
      // set default files tree items (root item) in nextTick.
      // Otherwise this.open isn't cleared properly (due to syncing perhaps)
      setTimeout(() => {
        this.items = [
          {
            type: 'root',
            extension: '',
            name: 'My Projects',
            children: []
          }
        ]
        this.initProjects(this.items[0])
      }, 0)
    },
    async initProjects (item) {
      this.$emit('loading', true)
      let url = this.endpoints.projects.url
      let response = await ApiService.query(url)
      // eslint-disable-next-line require-atomic-updates
      item.children = response.data.map(item => {
        item.type = 'dir'
        item.project_id = item.project_id.toString()
        item.children = []
        return item
      })
      this.$emit('loading', false)
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
      console.log('activeChanged', active)
      this.active = active
      let projectId = ''
      if (active.length) {
        projectId = active[0]
      }
      if (projectId) {
        const project = this.findChild(projectId)
        this.fetchProjectDocuments(project)
        this.setSelectedProjectItem(project)
      }
    },
    findChild (projectId) {
      const children = this.items[0].children
      const child = children.find((x) => x.project_id === projectId)
      return child
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
