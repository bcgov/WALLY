<template>
  <v-card class="watershedInfo" flat>
    <v-card-title
      class="title mt-5 ml-3 mr-3 pa-1 mb-2"
      dark>
      EFN Analysis
    </v-card-title>
    <v-card-text>
      <div>
        <p>
          Placeholder Text
        </p>
      </div>
    </v-card-text>
  </v-card>
</template>
<script>

import ApiService from '../../../../services/ApiService'
import qs from 'querystring'

export default {
  name: 'EfnAnalysis',
  components: {
  },
  props: ['efn_analysis'],
  data: () => ({
    efn_data: {}
  }),
  methods: {
    fetchEfnAnalysis () {
      const params = {
        placeholder: ''
      }
      ApiService.query(`/api/v1/efn/analysis?${qs.stringify(params)}`).then((r) => {
        const data = r.data
        this.efn_data = data.efn_data
      })
    }
  },
  mounted () {
    // this.fetchEfnAnalysis()
  }

}
</script>
