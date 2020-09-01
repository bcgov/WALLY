<template>
  <v-container class="pt-5">
    <v-toolbar flat>
      <v-banner color="indigo" icon="mdi-cloud-upload" icon-color="white" width="100%">
        <v-toolbar-title>Import a map layer</v-toolbar-title>
      </v-banner>
    </v-toolbar>
    <v-row class="pa-5">
      <v-col>
        <p>Import a map layer</p>
      </v-col>
      <v-col class="text-right">
        <v-col>
          <v-btn @click="upload()" color="primary" outlined>Upload a file</v-btn>
        </v-col>
      </v-col>
    </v-row>

      <div id="file-drag-drop">
        <form ref="fileform">
          <span class="drop-files"><v-icon>mdi-cloud-upload</v-icon> Drop the files here, or <a>browse</a></span>
        </form>
      </div>
  </v-container>
</template>
<style>
  #file-drag-drop form{
    display: block;
    height: 200px;
    width: 400px;
    background: #ccc;
    margin: auto;
    margin-top: 40px;
    text-align: center;
    line-height: 200px;
    border-radius: 4px;
  }
</style>
<script>
export default {
  name: 'Import Layer',
  data: () => ({
    buttonClicked: false,
    distance: 0,
    area: 0
  }),
  methods: {
    upload () {
      alert('Upload successful')
    }
  },
  computed: {
  },
  watch: {

  },
  mounted () {
  }

}
</script>

<style>
</style>
