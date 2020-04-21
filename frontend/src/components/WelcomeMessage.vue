<template>
  <v-dialog id="welcome-message" v-model="show.welcome_message" persistent max-width="1000">
    <v-card raised>
      <v-card-title class="headline">
        <span class="text-uppercase display-1">
          Water Allocation (WALLY)
        </span>
        <v-spacer></v-spacer>
        <v-btn
          icon
          @click="exit"
          color="white"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text class="mt-4">
        <p>
          Welcome to WALLY! This tool is intended to assist B.C. Government water allocation staff efficiently and effectively gather and analyze data and information in order to support robust and defensible water resource decisions. This tool is not designed to fetter or replace the decisions made by a statutory decision-maker.
        </p>
        <strong>
          Limitations
        </strong>
        <p>
          This tool aggregates diverse water data sources from various databases and applications and is limited by the data quality or other considerations associated to each data source. This application provides explanations about known data caveats and transparency in how data is accessed and transformed.  Throughout the application you will find many question mark icons that give more information about data sources, data limitations, and how data has been converted.
        </p>
        <div class="mb-3">
          <v-card outlined width="350" >
            <v-card-text >
            Where does this information come from?
            <v-icon color="primary">mdi-help-circle-outline</v-icon>
            </v-card-text>
          </v-card>
        </div>
        <strong>
          Disclaimer
        </strong>
        <p>
          This information is provided as a public service by the Government of British Columbia, Box 9411, Victoria, British Columbia, Canada V8W 9V1. This website and all of the information it contains are provided "as is" without warranty of any kind, whether express or implied. All implied warranties, including, without limitation, implied warranties of merchantability, fitness for a particular purpose, and non-infringement, are hereby expressly disclaimed.
        </p>
        <p>
          Links and references to any other websites are provided for information only and listing shall not be taken as endorsement of any kind. The Government of British Columbia is not responsible for the content or reliability of the linked websites and does not endorse the content, products, services or views expressed within them.
        </p>
        <p>
          Under no circumstances will the Government of British Columbia be liable to any person or business entity for any direct, indirect, special, incidental, consequential, or other damages based on any use of this website or any other website to which this site is linked, including, without limitation, any lost profits, business interruption, or loss of programs or information, even if the Government of British Columbia has been specifically advised of the possibility of such damages.

        </p>
      </v-card-text>
      <v-footer>
        <v-row
          justify="center"
        >
          <v-btn
            v-for="link in links"
            :key="link.text"
            text
            rounded
            :href="link.href"
            class="my-2"
          >
            {{ link.text }}
          </v-btn>
        </v-row>
      </v-footer>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn id="dont-show-again" color="primary" @click="hideByDefault">Don't show this again</v-btn>
      </v-card-actions>
    </v-card>

  </v-dialog>
</template>
<style lang="scss">
  #welcome-message{
    .headline{
      background-color: #036;
      color: white;
    }
  }
</style>
<script>
export default {
  name: 'WelcomeMessage',
  data: () => ({
    show: {
      welcome_message: (JSON.parse(localStorage.getItem('show_welcome_message')) == null) ? true : JSON.parse(localStorage.getItem('show_welcome_message'))
    },
    links: [
      {
        text: 'Copyright',
        href: 'https://www2.gov.bc.ca/gov/content/home/copyright'
      },
      {
        text: 'Disclaimer',
        href: 'https://www2.gov.bc.ca/gov/content/home/disclaimer'
      },
      {
        text: 'Privacy',
        href: 'https://www2.gov.bc.ca/gov/content/home/privacy'
      },
      {
        text: 'Accessibility',
        href: 'https://www2.gov.bc.ca/gov/content/home/accessible-government'
      }
    ]
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
