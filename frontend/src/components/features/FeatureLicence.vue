<template>
  <v-card elevation=0>
    <v-card-text>
      <div class="grey--text text--darken-4 headline" id="licenceTitle">{{ record.properties.LICENCE_NUMBER }} - {{ record.properties.POD_NUMBER }}</div>
      <div class="grey--text text--darken-2 title">Water Rights Licence</div>
      <v-divider></v-divider>
      <v-list dense class="mx-0 px-0">
        <v-list-item class="feature-content">
          <v-list-item-content>Licence number</v-list-item-content>
          <v-list-item-content>{{record.properties.LICENCE_NUMBER}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>POD number</v-list-item-content>
          <v-list-item-content>{{record.properties.POD_NUMBER}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>POD subtype</v-list-item-content>
          <v-list-item-content>{{record.properties.POD_SUBTYPE}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>POD status</v-list-item-content>
          <v-list-item-content>{{record.properties.POD_STATUS}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Licence status</v-list-item-content>
          <v-list-item-content>{{record.properties.LICENCE_STATUS}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Licence status date</v-list-item-content>
          <v-list-item-content>{{record.properties.LICENCE_STATUS_DATE}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Well tag number</v-list-item-content>
          <v-list-item-content>
            <a
                v-if="record.properties.WELL_TAG_NUMBER"
                :href="`https://apps.nrs.gov.bc.ca/gwells/well/${record.properties.WELL_TAG_NUMBER}`"
            >
              {{record.properties.WELL_TAG_NUMBER}}
            </a>
          </v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>File number</v-list-item-content>
          <v-list-item-content>{{record.properties.FILE_NUMBER}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Purpose use</v-list-item-content>
          <v-list-item-content>{{record.properties.PURPOSE_USE}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Rediversion ind</v-list-item-content>
          <v-list-item-content>{{record.properties.REDIVERSION_IND}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Quantity</v-list-item-content>
          <v-list-item-content>{{record.properties.QUANTITY}} {{record.properties.QUANTITY_UNITS}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Hydraulic connectivity</v-list-item-content>
          <v-list-item-content>{{record.properties.HYDRAULIC_CONNECTIVITY}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Primary licensee name</v-list-item-content>
          <v-list-item-content>{{record.properties.PRIMARY_LICENSEE_NAME}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Source name</v-list-item-content>
          <v-list-item-content>{{record.properties.SOURCE_NAME}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Data source:</v-list-item-content>
          <v-list-item-content><a href="https://catalogue.data.gov.bc.ca/dataset/water-rights-licences-public" target="_blank">DataBC Water Rights Licences</a></v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>
            <dl>
              <template v-for="(doc, i) in documents">
                <dt :key="i">{{ doc.description }}</dt>
                <dd :key="i"><a :href="doc.downloadurl">{{ doc.downloadurl }}</a></dd>
              </template>
            </dl>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
import axios from 'axios'

export default {
  name: 'FeatureLicence',
  props: {
    record: Object
  },
  data () {
    return {
      loading: false,
      documents: []
    }
  },
  computed: {
    licenceNumber () {
      return this.record.properties.LICENCE_NUMBER
    },
    licenceWithoutChars () {
      return this.record.properties.LICENCE_NUMBER.replace(/D+/g, '')
    }
  },
  methods: {
    fetchDocuments () {
      axios.get(`https://j200.gov.bc.ca/ws/RestGWellsInterface/licence/${this.licenceWithoutChars}`).then((r) => {
        this.documents = r.data
      }).catch((e) => {
        console.error(e)
      })
    }
  },
  mounted () {
    this.fetchDocuments()
  }
}
</script>

<style>

</style>
