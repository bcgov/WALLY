<template>
  <v-app>
  <div>
    <label>
      <input type="radio" name="radio" value="test"/>
      My old radio button
    </label>
    <v-container>
    <v-radio-group
      v-model="radios"
      mandatory
    >
      <v-radio
        label="Radio 1"
        value="radio-1"
      ></v-radio>
      <v-radio
        label="Radio 2"
        value="radio-2"
      ></v-radio>
    </v-radio-group>
    <v-radio-group v-model="radioGroup">
    <v-radio
      v-for="n in optionsCount"
      :key="n"
      :label="`Radio ${n}`"
      :value="n"
    ></v-radio>
  </v-radio-group>
    </v-container>
  </div>
  </v-app>

</template>

<script>

export default {
  name: 'RadioButton',

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
      radioGroup: 1,
      radios: null
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
