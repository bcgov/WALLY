<template>
  <v-dialog v-model="show.welcome_message" persistent max-width="1000">
  <v-card id="allocationTable">
    <v-card-title class="headline">
      Welcome to WALLY
      <v-spacer></v-spacer>
      <v-btn
        icon
        @click="exit"
      >
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-card-title>
    <v-card-text>
      Hello World
    </v-card-text>
    <v-card-actions>
      <v-btn @click="hideByDefault">Don't show this again</v-btn>
    </v-card-actions>
  </v-card>
  </v-dialog>
</template>
<script>
export default {
  name: 'WelcomeMessage',
  data: () => ({
    show: {
      welcome_message: (JSON.parse(localStorage.getItem('show_welcome_message')) == null) ? true : JSON.parse(localStorage.getItem('show_welcome_message'))
    }
  }),
  methods: {
    exit () {
      this.$emit('close', false)
      this.show.welcome_message = false
    },
    hideByDefault () {
      localStorage.setItem('show_welcome_message', JSON.stringify(false))
      this.show.welcome_message = false
    }
  }
}
</script>
