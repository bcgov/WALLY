<template>
  <header>
    <div class="banner">
        <a href="https://gov.bc.ca" alt="British Columbia">
          <img :src="require('../assets/bcgov_logo.svg')" height="40" max-width="150" alt="Go to the Government of British Columbia website" />
        </a>
        <h1>Water Allocation</h1>
        <div aria-label="This application is currently in Beta phase" class=Beta-PhaseBanner>
          Beta
        </div>
    </div>
    <div class="other">
    <!--
      This place is for anything that needs to be right aligned
      beside the logo.
    -->
      {{ name }}
    </div>
  </header>
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
    }
  },
  created () {
    this.name = this.$auth.name
    EventBus.$on('auth:update', this.setName)
  },
  beforeDestroy () {
    EventBus.$off('auth:update', this.setName)
  }
}
</script>
<style>
header {
  background-color: #036!important;
  border-bottom: 2px solid #fcba19;
  padding: 0 65px 0 65px;
  color: #fff;
  display: flex;
  height: 65px;
  top: 0px;
  width: 100%;
}

header h1 {
  font-family: ‘Noto Sans’, Verdana, Arial, sans-serif;
  font-weight: normal;  /* 400 */
  margin: 5px 5px 0 18px;
  visibility: hidden;
}

header .banner {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  margin: 0 10px 0 0;
  /* border-style: dotted;
  border-width: 1px;
  border-color: lightgrey; */
}

header .other {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  flex-grow: 1;
  font-weight: bold;
  /* border-style: dotted;
  border-width: 1px;
  border-color: lightgrey; */
}

.Beta-PhaseBanner {
  color: #fcba19;
  margin-top: -1em;
  text-transform: uppercase;
  font-weight: 600;
  font-size: 16px;
  visibility: hidden;
}

:focus {
    outline: 4px solid #3B99FC;
    outline-offset: 1px;
  }

@media screen and (min-width: 600px) {
  .Beta-PhaseBanner {
    visibility: visible;
  }
}

@media screen and (min-width: 600px) and (max-width: 899px) {
  header h1 {
    font-size: calc(7px + 2.2vw);
    visibility: visible;
  }
}

@media screen and (min-width: 900px) {
  header h1 {
    font-size: 2.0em;
    visibility: visible;
  }
}
</style>
