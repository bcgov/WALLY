<template>
  <v-app-bar
    clipped-left
    app
    color="#036"
    dark
    height="64"
    id="wally-header"
  >
    <img
      class="ml-5"
      :src="require('../assets/bcgov_logo.svg')"
      height="40" max-width="150"
      alt="Go to the Government of British Columbia website" />
    <v-toolbar-title class="bcgov-title">
      Water Allocation
    </v-toolbar-title>
    <p class="ml-2" v-if="appInfo && appInfo.wally_env && appInfo.wally_env.toLowerCase() !== 'production'">
      {{appInfo.wally_env === 'DEV' ? 'Development' : 'Staging'}} Environment
    </p>
    <div class="flex-grow-1">
    </div>
    <!-- <div class="my-2 mr-3">
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn small color="primary" v-on="on" @click="openFeedback()">Send Feedback</v-btn>
        </template>
        <span>Please send us any feedback or ideas you may have on how we can improve the app.</span>
      </v-tooltip>
    </div> -->
    <div class="wally-user mr-5">{{ name }}</div>
    <div>
      <v-menu offset-y min-width="300">
        <template v-slot:activator="{ on }">
          <v-btn
            v-on="on"
            icon
          >
            <v-icon>mdi-menu</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item
            v-for="(item, index) in menuItems"
            :key="index"
            @click="item.action()"
          >
            <v-list-item-content>
              <v-list-item-title>{{item.title}}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-dialog v-model="show.about" width="600px">
        <v-card>
          <v-card-title class="headline">
            About Water Allocation (WALLY)
          </v-card-title>
          <v-card-text v-if="appInfo">
            Version Number: {{appInfo && appInfo.wally_version}}
          </v-card-text>
        </v-card>
      </v-dialog>
      <!-- <v-switch :label="sidePanelFeatureLabel" :input-value="this.adjustableSidePanel" @change="this.toggleAdjustableSidePanel"></v-switch> -->
    </div>
  </v-app-bar>
</template>

<script>
import EventBus from '../services/EventBus.js'
import { mapGetters } from 'vuex'

export default {
  name: 'Header',
  props: ['appInfo'],
  data () {
    return {
      name: '',
      menuItems: [
        {
          title: 'About WALLY',
          name: 'about',
          action: () => this.openDialog()
        },
        {
          title: 'Logout',
          name: 'logout',
          action: () => this.logout()
        }
      ],
      show: {
        about: false
      }
    }
  },
  computed: {
    ...mapGetters([
      'adjustableSidePanel'
    ]),
    sidePanelFeatureLabel () {
      return this.adjustableSidePanel ? 'Adjustable Side Panel' : 'Responsive Panel'
    }
  },
  methods: {
    logout () {
      this.$auth.logout()
    },
    openDialog () {
      this.show.about = true
    },
    toggleAdjustableSidePanel () {
      global.config.debug && console.log('[wally] toggling')
      this.$store.commit('toggleAdjustableSidePanel')
    },
    updateAuth (payload) {
      const { name, authenticated } = payload
      if (authenticated) {
        // Set the user's name
        this.name = name
      }
    },
    // Commented out until new product owner is found for WALLY
    // openFeedback () {
    //   window.location = 'mailto:CHANGEME@gov.bc.ca;CHANGEME@gov.bc.ca?subject=Wally Feedback'
    // }
  },
  created () {
    this.name = (this.$auth && this.$auth.name) || '' // fallback value if auth status not yet available
    EventBus.$on('auth:update', this.updateAuth)
  },
  beforeDestroy () {
    EventBus.$off('auth:update', this.updateAuth)
  }
}
</script>
<style lang="scss">
#wally-header {
  box-shadow: inset 0 -1px 0 #fcba19;
}
.bcgov-title {
  font-weight: normal;
  font-size: 28px;
  margin: 5px 5px 0 18px;
  visibility: hidden;
}
.beta-banner {
  color: #fcba19;
  text-transform: uppercase;
  font-weight: 600;
  font-size: 16px;
  visibility: hidden;
}
.wally-user {
  visibility: hidden;
}
@media screen and (min-width: 600px) {
  .beta-banner {
    visibility: visible;
  }
}

@media screen and (min-width: 600px) and (max-width: 899px) {
  .bcgov-title {
    font-size: calc(7px + 2.2vw);
    visibility: visible;
  }
}

@media screen and (min-width: 900px) {
  .bcgov-title {
    font-size: 2.0em;
    visibility: visible;
  }
  .wally-user {
    visibility: visible;
  }
}

.v-input--switch label{
   width: 100px;
   font-size: smaller;
 }
</style>
