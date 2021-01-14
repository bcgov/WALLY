<template>
  <v-row>
    <v-col
      cols="12"
      class="py-2"
    >
      <p>Text Options</p>

      <v-btn-toggle
        v-model="text"
        tile
        color="deep-purple accent-3"
        group
      >
        <v-btn value="left">
          Left
        </v-btn>

        <v-btn value="center">
          Center
        </v-btn>

        <v-btn value="right">
          Right
        </v-btn>

        <v-btn value="justify">
          Justify
        </v-btn>
      </v-btn-toggle>
    </v-col>
    <v-col>
      <v-btn-toggle v-model="toggle_exclusive">
        <v-btn>
          Left option
        </v-btn>

        <v-btn>
          Right option
        </v-btn>
      </v-btn-toggle>
    </v-col>
  </v-row>
</template>
<script>

export default {
  name: 'ButtonGroup',

  props: {
    primary: {
      type: Boolean,
      default: false
    },
    size: {
      type: String,
      default: 'medium',
      validator: function (value) {
        return ['small', 'medium', 'large'].indexOf(value) !== -1
      }
    },
    optionsCount: {
      type: String,
      required: true
    },
    backgroundColor: {
      type: String
    }
  },

  data () {
    return {
      toggle_exclusive: 1
    }
  },

  computed: {
    classes () {
      return {
        'storybook-button': true,
        'storybook-button--primary': this.primary,
        'storybook-button--secondary': !this.primary,
        [`storybook-button--${this.size}`]: true
      }
    },
    style () {
      return {
        backgroundColor: this.backgroundColor
      }
    }
  },

  methods: {
    onClick () {
      this.$emit('onClick')
    }
  }
}
</script>
