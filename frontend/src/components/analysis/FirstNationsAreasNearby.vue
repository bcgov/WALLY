<template>
  <v-container class="pa-0 ma-0">
    <v-card outlined>
      <v-card-text class="grey--text text--darken-4">
        <div class="subtitle-1 mt-5">Nearest Communities</div>
        <dl id="nearestCommunities">
          <template v-for="(c, i) in communities">
          <dt :key="`communityName${i}`">
            {{c.FIRST_NATION_BC_NAME}} ({{(c.distance / 1000).toFixed(1)}} km)
          </dt>
          <dd :key="`communityLink${i}`"><a :href="c.URL_TO_BC_WEBSITE" target="_blank">{{c.URL_TO_BC_WEBSITE}}</a></dd>
          </template>
          <template v-if="communities.length === 0 && !loading">None found.</template>
        </dl>
        <div class="subtitle-1 mt-5">Treaty areas</div>
        <dl id="nearestTreatyAreas">
          <template v-for="(area, i) in areas">
          <dt :key="`areaTreaty${i}`">
            {{area.TREATY}} - {{area.AREA_TYPE}} ({{ (area.distance / 1000).toFixed(1) }} km)
          </dt>
          <dd :key="`areaName${i}`">{{ area.FIRST_NATION_NAME }}</dd>
          <dd :key="`areaDate${i}`">Effective date: {{ area.EFFECTIVE_DATE | readableDate }}</dd>
          </template>
          <template v-if="areas.length === 0 && !loading">None found.</template>
        </dl>
        <div class="subtitle-1 mt-5">Treaty lands</div>
        <dl id="nearestTreatyLands">
          <template v-for="(land, i) in lands">
          <dt :key="`landTreaty${i}`">
            {{land.TREATY}} - {{ land.LAND_TYPE }} ({{(land.distance / 1000).toFixed(1)}} km)
          </dt>
          <dd :key="`landName${i}`">{{ land.FIRST_NATION_NAME }}</dd>
          <dd :key="`landDate${i}`">Effective date: {{ land.EFFECTIVE_DATE | readableDate }}</dd>
          </template>
          <template v-if="lands.length === 0 && !loading">None found.</template>
        </dl>
      </v-card-text>

    </v-card>

    <v-expansion-panels class="mt-5 elevation-0" multiple>
      <v-expansion-panel class="elevation-0">
        <v-expansion-panel-header disable-icon-rotate class="grey--text text--darken-4 subtitle-1">
          Where does this information come from?
          <template v-slot:actions>
            <v-icon color="primary">mdi-help-circle-outline</v-icon>
          </template>

        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <dl>
            <dt>First Nations Community Locations</dt>
            <dd>
              <a href="https://catalogue.data.gov.bc.ca/dataset/first-nation-community-locations" target="_blank">
                https://catalogue.data.gov.bc.ca/dataset/first-nation-community-locations
              </a>
            </dd>
            <dt>First Nations Treaty Areas</dt>
            <dd>
              <a href="https://catalogue.data.gov.bc.ca/dataset/first-nations-treaty-areas" target="_blank">
                https://catalogue.data.gov.bc.ca/dataset/first-nations-treaty-areas
              </a>
            </dd>
            <dt>First Nations Treaty Lands</dt>
            <dd>
              <a href="https://catalogue.data.gov.bc.ca/dataset/first-nations-treaty-lands" target="_blank">
                https://catalogue.data.gov.bc.ca/dataset/first-nations-treaty-lands
              </a>
            </dd>
          </dl>
          <dl>
            <dt>Nearest Communities</dt>
            <dd>Nearest communities are determined by the distance from the selected feature to the location of the community listed in the
              <a href="https://catalogue.data.gov.bc.ca/dataset/first-nation-community-locations" target="_blank">First Nations Community Locations</a>
              dataset. The main community may be within a selection area, in which case, the distance will be shown as 0 km.</dd>
            <dt>Nearest Treaty Areas and Nearest Treaty Lands</dt>
            <dd>The nearest Treaty Areas and nearest Treaty Lands are determined by the closest distance between the selection area and the Treaty Areas and Treaty Lands defined in the
              <a href="https://catalogue.data.gov.bc.ca/dataset/first-nations-treaty-areas" target="_blank">First Nations Treaty Areas</a> and
              <a href="https://catalogue.data.gov.bc.ca/dataset/first-nations-treaty-lands" target="_blank">First Nations Treaty Lands</a>
              datasets. If any part of the selection area overlaps a Treaty Area or Treaty Land, the distance will be shown as 0 km.
            </dd>
          </dl>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>

  </v-container>
</template>

<script>
import ApiService from '../../services/ApiService'
import qs from 'querystring'
import bbox from '@turf/bbox'
import bboxPolygon from '@turf/bbox-polygon'
import moment from 'moment'

export default {
  name: 'FirstNationsAreasNearby',
  props: ['record'],
  data: () => ({
    communities: [],
    areas: [],
    lands: [],
    loading: false
  }),
  computed: {
    bounds () {
      return bboxPolygon(bbox(this.record.geometry)).geometry
    }
  },
  filters: {
    readableDate (val) {
      return moment(val, 'YYYYMMDD').format('MMMM Do YYYY')
    }
  },
  methods: {
    resetNearestAreas () {
      this.communities = []
      this.areas = []
      this.lands = []
    },
    fetchNearbyFirstNationsAreas () {
      this.loading = true
      this.resetNearestAreas()
      const params = {
        geometry: JSON.stringify(this.bounds)
      }
      ApiService.query(`/api/v1/analysis/firstnations/nearby?${qs.stringify(params)}`).then((r) => {
        this.communities = r.data.nearest_communities
        this.areas = r.data.nearest_treaty_areas
        this.lands = r.data.nearest_treaty_lands
      }).catch((e) => {
        console.error(e)
      }).finally(() => {
        this.loading = false
      })
    }
  },
  watch: {
    record: {
      handler () {
        this.fetchNearbyFirstNationsAreas()
      },
      deep: true
    }
  },
  mounted () {
    this.fetchNearbyFirstNationsAreas()
  }
}
</script>

<style>

</style>
