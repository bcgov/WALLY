<template>
  <v-dialog v-model="dialog" width="650">
    <template v-slot:activator="{ on, attrs }">
      <v-icon
        v-on="on"
        class='mr-1'>
        mdi-square-edit-outline
      </v-icon>
    </template>

    <v-card shaped>
      <v-card-title class="headline grey lighten-3" primary-title>
          Edit Analysis
      </v-card-title>
      <v-card-text class="mt-4">
        <v-row>
          <v-col cols="12" md="12" align-self="center">
            <v-text-field
              label="Saved Analysis Name"
              placeholder="Enter a name for this saved analysis"
              :rules="[rules.required, rules.length]"
              v-model="editAnalysis.name"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="12">
            <v-text-field
              label="Saved Analysis Description"
              placeholder="Enter a description of the analysis"
              v-model="editAnalysis.description"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          outlined
          @click="editSavedAnalysisRecord"
          color="primary"
          :disabled="loading"
        >
          <div v-if="!loading">
            Save
          </div>
          <v-progress-circular
            v-if="loading"
            indeterminate
            size=24
            class="ml-1"
            color="primary"
          ></v-progress-circular>
        </v-btn>

      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import ApiService from '../../services/ApiService'
export default {
  name: 'SavedAnalysesEditModal',
  props: ['analysis'],
  data: function () {
    return {
      loading: false,
      dialog: false,
      editAnalysis: Object.assign({}, this.analysis),
      rules: {
        required: value => !!value || 'Name is Required.',
        length: value => value.length > 2 || 'Name requires more than 3 characters.'
      }
    }
  },
  computed: {
    ...mapGetters('map', ['map', 'activeMapLayers'])
  },
  methods: {
    ...mapActions(['getSavedAnalyses', 'editSavedAnalyses']),
    editSavedAnalysisRecord () {
      let uuid = this.editAnalysis.saved_analysis_uuid
      let name = this.editAnalysis.name
      let description = this.editAnalysis.description
      console.log(uuid, name, description)

      if (this.editAnalysis.name.length < 3) {
        return
      }

      this.loading = true
      const params = {
        name: name,
        description: description
      }

      console.log(params, uuid)

      ApiService.put(`/api/v1/saved_analyses/${uuid}`, params)
        .then((r) => {
          this.dialog = false
          this.loading = false
          this.getSavedAnalyses()
        }).catch((e) => {
          this.loading = false
          console.log('error editing saved analyses', e)
        })
    }
  }
}
</script>

<style>
</style>
