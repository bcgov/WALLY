<template>
    <v-app-bar
      clipped-left
      app
      color="#036"
      dark
      height="64"
      class="wally-header"
    >
      <img
        class="ml-5"
        :src="require('../assets/bcgov_logo.svg')"
        height="40" max-width="150"
        alt="Go to the Government of British Columbia website" />
      <v-toolbar-title class="bcgov-title">Water Allocation

      </v-toolbar-title>
      <span aria-label="This application is currently in Alpha phase" class="beta-banner">
          Alpha
      </span>
      <div class="flex-grow-1"></div>
      <div class="my-2 mr-3">
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn small color="primary" v-on="on" @click="openFeedback()">Send Feedback</v-btn>
          </template>
          <span>Please send us any feedback or ideas you may have on how we can improve the app.</span>
        </v-tooltip>
      </div>
      <div class="wally-user mr-5">{{ name }}</div>
    </v-app-bar>
</template>

<script>
import EventBus from '../services/EventBus.js'

export default {
  name: 'Header',
  data () {
    return {
      name: ''
    }
  },
  methods: {
    setName (payload) {
      const { name, authenticated } = payload
      if (authenticated) {
        this.name = name
      }
    },
    openFeedback () {
      window.location = 'mailto:kailee.douglas@gov.bc.ca lindsay.macfarlane@gov.bc.ca?subject=Wally Feedback'
    }
  },
  created () {
    this.name = (this.$auth && this.$auth.name) || '' // fallback value if auth status not yet available
    EventBus.$on('auth:update', this.setName)
  },
  beforeDestroy () {
    EventBus.$off('auth:update', this.setName)
  }
}
</script>
<style>
  .wally-header {
    box-shadow: inset 0 -1px 0 #fcba19;
  }
.bcgov-title {
  font-family: ‘Noto Sans’, Verdana, Arial, sans-serif;
  font-weight: normal;
  font-size: 28px;
  margin: 5px 5px 0 18px;
  visibility: hidden;
}
.beta-banner {
  color: #fcba19;
  margin-top: -0.5em;
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
</style>
