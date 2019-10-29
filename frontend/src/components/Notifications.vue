<template>
  <div>
    <!-- app error popup -->
    <v-snackbar v-model="error" color="error" bottom right :timeout="6000" id="errorNotification">
      <div v-if="errorMsg">{{ errorMsg }}</div>
      <div v-else>There was an error reaching the server. Please try again later.</div>
      <v-btn
        dark
        text
        @click="clearError"
      >
        Close
      </v-btn>
    </v-snackbar>

    <!-- app info e.g. hints that don't need to be an error message -->
    <v-snackbar v-model="info" color="info" bottom left :timeout="6000" id="infoNotification">
      <div v-if="infoMsg">{{ infoMsg }}</div>
      <v-btn
        dark
        text
        @click="clearInfo"
      >
        Close
      </v-btn>
    </v-snackbar>

    <!-- help on features -->
    <v-snackbar v-model="help" color="info" bottom left vertical :timeout="15000" id="helpNotification">
      <div v-if="helpMsg && helpMsg.text">{{ helpMsg.text }}</div>
      <div class="d-flex">
        <v-btn
          dark
          text
          id="disableHelpButton"
          @click="disableHelp(helpMsg.disableKey)"
        >
          Don't show again
        </v-btn>
        <v-btn
          dark
          text
          class="mx-5"
          @click="clearHelp"
        >
          Close
        </v-btn>

      </div>
    </v-snackbar>
  </div>
</template>

<script>
import EventBus from '../services/EventBus'
export default {
  name: 'Notifications',
  data: () => ({
    error: false,
    errorMsg: '',
    info: false,
    infoMsg: '',
    help: false,
    helpMsg: {} // should contain a "text" key and a "disableKey" key (for disabling that message)
  }),
  methods: {
    clearError () {
      this.error = false
      this.errorMsg = ''
    },
    setError (msg) {
      this.clearError()
      this.error = !!msg

      // the error popup has a generic message if a specific string
      // wasn't included as the event payload. However, if a msg exists,
      // it's set here.
      if (msg && msg !== true) {
        this.errorMsg = msg
      }
    },
    clearInfo () {
      this.info = false
      this.infoMsg = ''
    },
    setInfo (msg) {
      this.clearInfo()

      // unlike errors, there is no "general" info message when
      // a msg string not provided. Ensure that the `info` event
      // has a payload with a message.
      if (msg && msg !== true) {
        this.info = !!msg
        this.infoMsg = msg
      } else {
        console.error('info event triggered without an info message as the payload')
      }
    },
    clearHelp () {
      this.help = false
      this.helpMsg = {}
    },
    setHelp (payload) {
      if (payload.disableKey && JSON.parse(localStorage.getItem(payload.disableKey)) === true) {
        // check if this help message has been disabled by the user.
        // help messages are (currently) disabled on an message by message basis, not for all help messages.
        return
      } else if (!payload.disableKey) {
        console.error('help event triggered without a payload object containing `disableKey` (to allow the user to disable this message)')
      }

      this.clearHelp()

      if (payload.text && payload.text !== true) {
        this.help = true
        this.helpMsg = payload
      } else {
        console.error('help event triggered without a payload object containing a `text` property')
      }
    },
    disableHelp (key) {
      // disables a specific help message ("don't show again")
      localStorage.setItem(key, JSON.stringify(true))
      this.clearHelp()
    }
  },
  mounted () {
    EventBus.$on('error', this.setError)
    EventBus.$on('info', this.setInfo)
    EventBus.$on('help', this.setHelp)
  },
  beforeDestroy () {
    EventBus.$off('error', this.setError)
    EventBus.$off('info', this.setInfo)
    EventBus.$off('help', this.setHelp)
  }
}
</script>

<style>

</style>
