<template>
  <v-toolbar-items class="py-1">
    <v-btn @click="takeScreenshot" color="blue-grey" dark tile icon>
      <v-icon>mdi-camera</v-icon>
    </v-btn>
  </v-toolbar-items>
</template>

<script>
import { mapGetters } from 'vuex'
import html2canvas from 'html2canvas'
import { saveAs } from 'file-saver'
export default {
  name: 'Screenshot',
  computed: {
    ...mapGetters('map', [
      'map'
    ])
  },
  methods: {
    takeScreenshot () {
      this.downloadMapImage()
    },
    downloadMapImage () {
      // Custom Metrics - Screen capture
      window._paq && window._paq.push(['trackEvent', 'Screenshot', 'Capture screenshot', 'map'])
      const filename = 'map--'.concat(new Date().toISOString()) + '.png'
      html2canvas(this.map._container).then(canvas => {
        canvas.toBlob(function (blob) {
          saveAs(blob, filename)
        })
      })
    }
  }
}
</script>
