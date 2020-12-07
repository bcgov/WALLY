<template>
  <div>
<!--    <div v-for="(processedFile,i) in files.filter(x => x.status)" :key="`fileMsg${i}`">-->
<!--      <v-alert-->
<!--        :id="`statusMessage${i}`"-->
<!--        v-if="processedFile.message"-->
<!--        :type="processedFile.status"-->
<!--      >-->
<!--        {{ processedFile.message }}-->
<!--        <span class="float-right" v-if="processedFile.firstFeatureCoords">-->
<!--          <v-tooltip bottom>-->
<!--            <template v-slot:activator="{ on }">-->
<!--               <v-btn text small v-on="on" @click="map.flyTo({center: processedFile.firstFeatureCoords})">-->
<!--                 <v-icon small>mdi-arrow-top-right</v-icon>-->
<!--               </v-btn>-->
<!--            </template>-->
<!--            <span>Fly to visible features on this layer</span>-->
<!--          </v-tooltip>-->
<!--        </span>-->
<!--      </v-alert>-->
<!--    </div>-->
    <div v-for="(successFile, i) in files.success" :key="`successFileMsg${i}`">
      <v-alert
        :id="`statusMessage${i}`"
        v-if="successFile.message"
        :type="successFile.status"
      >
        {{ successFile.message }}
        <span class="float-right" v-if="successFile.firstFeatureCoords">
          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
               <v-btn text small v-on="on" @click="map.flyTo({center: successFile.firstFeatureCoords})">
                 <v-icon small>mdi-arrow-top-right</v-icon>
               </v-btn>
            </template>
            <span>Fly to visible features on this layer</span>
          </v-tooltip>
        </span>
      </v-alert>
    </div>
    <div v-for="(errorFile,i) in files.error" :key="`errorFileMsg${i}`">
      <v-alert
        :id="`statusMessage${i}`"
        v-if="errorFile.message"
        :type="errorFile.status"
      >
        {{ errorFile.message }}
      </v-alert>
    </div>
    <div v-for="(warningFile,i) in files.warning" :key="`warningFileMsg${i}`">
      <v-alert
        :id="`statusMessage${i}`"
        v-if="warningFile.message"
        :type="warningFile.status"
      >
        {{ warningFile.message }}
      </v-alert>
    </div>
  </div>
</template>
<script>
import { mapGetters } from 'vuex'

export default {
  name: 'FileListProcessed',
  props: ['files'],
  computed: {
    ...mapGetters('map', ['map'])
  }
}
</script>
