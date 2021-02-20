<template>
  <v-card>
    <v-toolbar color="primary" dark flat>
      <v-icon>mdi-silverware</v-icon>
      <v-toolbar-title>Project Documents</v-toolbar-title>
    </v-toolbar>

    <v-row>
      <v-col>
        <v-card-text>
          <v-treeview
            v-model="tree"
            :load-children="fetch"
            :items="documents"
            selected-color="indigo"
            open-on-click
            selectable
            return-object
            expand-icon="mdi-chevron-down"
            on-icon="mdi-bookmark"
            off-icon="mdi-bookmark-outline"
            indeterminate-icon="mdi-bookmark-minus"
          >
          </v-treeview>
        </v-card-text>
      </v-col>

      <v-divider vertical></v-divider>

      <!-- <v-col cols="12" md="6">
        <v-card-text>
          <div
            v-if="tree.length === 0"
            key="title"
            class="title font-weight-light grey--text pa-4 text-center"
          >
            Select your documents
          </div>

          <v-scroll-x-transition group hide-on-leave>
            <v-chip
              v-for="(selection, i) in tree"
              :key="i"
              color="grey"
              dark
              small
              class="ma-1"
            >
              <v-icon left small> mdi-beer </v-icon>
              {{ selection.name }}
            </v-chip>
          </v-scroll-x-transition>
        </v-card-text>
      </v-col> -->
    </v-row>

    <v-divider></v-divider>

    <v-card-actions>
      <v-btn text @click="tree = []"> Reset </v-btn>

      <v-spacer></v-spacer>

      <v-btn class="white--text" color="green darken-1" depressed>
        Save
        <v-icon right> mdi-content-save </v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
// import ApiService from '../../services/ApiService'

export default {
  data: () => ({
    documents: [],
    isLoading: false,
    tree: [],
    types: []
  }),

  computed: {
    items () {
      const children = this.types.map((type) => ({
        id: type,
        name: this.getName(type),
        children: this.getChildren(type)
      }))

      return [
        {
          id: 1,
          name: 'All documents',
          children
        }
      ]
    },
    shouldShowTree () {
      return this.documents.length > 0 && !this.isLoading
    }
  },

  watch: {
    documents (val) {
      this.types = val
        .reduce((acc, cur) => {
          const type = cur.brewery_type

          if (!acc.includes(type)) acc.push(type)

          return acc
        }, [])
        .sort()
    }
  },

  methods: {
    fetch () {
      if (this.documents.length) return

      // ApiService.query(`/api/v1/projects/${this.project_id}/documents/`)
      //   .then((r) => {
      //     console.log(r.data)
      //     this.documents = r.data
      //     this.loading = false
      //   })
      //   .catch((e) => {
      //     this.loading = false
      //     console.error(e)
      //   })

      this.documents = [
        {
          name: 'test 1'
        },
        {
          name: 'test 2'
        }
      ]
    },
    getChildren (type) {
      const documents = []

      for (const document of this.documents) {
        if (document.document_type !== type) continue

        documents.push({
          ...document,
          name: this.getName(document.name)
        })
      }

      return documents.sort((a, b) => {
        return a.name > b.name ? 1 : -1
      })
    },
    getName (name) {
      return `${name.charAt(0).toUpperCase()}${name.slice(1)}`
    }
  }
}
</script>
