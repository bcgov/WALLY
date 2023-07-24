<template>
  <div>
    <v-card outlined v-if="droppedFiles.length > 0 && queuedFiles.length === 0" class="pa-2 mb-5">
      <h3>Files to be processed</h3>
      <v-card flat v-for="(file, index) in droppedFiles" class="" v-bind:key="index" id="droppedFileList">
            {{file.name}}
        <v-progress-linear v-if="isFileLoading(file.name)" show indeterminate></v-progress-linear>
      </v-card>
    </v-card>
    <v-card outlined v-for="(file, index) in queuedFiles" class="mb-5 pa-5" v-bind:key="index" id="fileList">
      <dl>
        <dt>
          Filename(s):
        </dt>
        <dd>
          {{file.name}}
        </dd>
      </dl>
      <v-progress-linear v-if="isFileLoading[file.name]" show indeterminate></v-progress-linear>
      <dl v-if="file && file.name && file.stats">
        <dt>
          Colour:
        </dt>
        <dd>
          <v-color-picker
            hide-canvas
            hide-inputs
            v-model="file.color"
            flat
          ></v-color-picker>
        </dd>
        <dt>
          Size:
        </dt>
        <dd>
          {{ file.stats.size ? `${(file.stats.size / 1e6).toFixed(2)} MB` : '' }}
          <v-icon
            v-if="file && file.stats && file.stats.size > warnFileSizeThreshold"
            color="orange"
            small
          >mdi-alert</v-icon>
        </dd>
        <dt>
          Geometry type:
        </dt>
        <dd> {{ file.stats.geomType }}</dd>
        <dt>Total features:</dt>
        <dd>{{file.stats.numFeatures}}</dd>
        <dt v-if="file.stats.propertyFields">
          Feature properties:
        </dt>
        <dd>
          <v-row>
            <v-col>
              <div v-if="!file.options.showAllProperties">{{file.stats.propertyFields.length}} properties</div>
              <div v-else>
                <div v-for="prop in file.stats.propertyFields" :key="`${file.name}${prop}`">{{prop}}</div>
              </div>
            </v-col>
            <v-btn dense outlined color="primary" @click="file.options.showAllProperties = !file.options.showAllProperties">
              {{file.options.showAllProperties ? 'Hide' : 'Show'}}
            </v-btn>
            <v-col cols="2"></v-col>
          </v-row>
        </dd>
      </dl>
      <v-alert
        class="my-3"
        :id="`fileSizeWarning${index}`"
        v-if="file && file.size > warnFileSizeThreshold"
        type="warning"
      >
        {{file.name}}: file size greater than 10 MB. This file may take additional time to load and it may cause performance issues.
      </v-alert>
    </v-card>
  </div>
</template>
<style lang="scss">
  #fileList, #droppedFileList{
    dl {
      display: flex;
      flex-wrap: wrap;
      padding-bottom: 10px;
    }

    dt {
      width: 33%;
      margin-top: 0;
      border-bottom: 1px solid lightgrey;
    }

    dd {
      padding-left: 10px;
      width: 66%;
      border-bottom: 1px solid lightgrey;
    }

    dt:nth-child(n+3):nth-last-child(2),
    dd:nth-child(n+3):last-child {
      border-bottom: none;
    }

    dd, dt {
      margin-top: 5px;
    }
  }
</style>
<script>
import { mapGetters } from 'vuex'

export default {
  name: 'FileList',
  props: ['droppedFiles'],
  data: () => ({
    warnFileSizeThreshold: global.config.warnUploadFileSizeThresholdInMB * 1024 * 1024
  }),
  computed: {
    ...mapGetters('importer', ['isFileLoading', 'queuedFiles'])
  }
}
</script>
