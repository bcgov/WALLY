<template>
  <v-form>
    <v-card class="mb-5 pa-5" outlined tile>
    <v-row>
      <div class="subtitle-1">Select time period to consider</div>
    </v-row>
    <v-row>
      <div class="body-2">Select the time to consider where pumping rate (Q) is varied and time (T) is constant</div>
    </v-row>
    <v-row>
      <v-col
        cols="4"
        class="py-2"
      >

        <v-text-field
          label="Select time period to consider"
          hint="Select the time to consider where pumping rate (Q) is varied and time (T) is constant"
          suffix="days"
          persistent-hint
          required>
        </v-text-field>
      </v-col>
      <v-col cols="6">
        <v-btn-toggle v-model="toggle_exclusive">
          <v-btn small>
            Latest time considered
          </v-btn>
          <v-btn small>
            Earliest time considered
          </v-btn>
        </v-btn-toggle>
      </v-col>
    </v-row>
    </v-card>
    <v-card class="mt-5 pa-5" outlined tile>
    <v-row>
      <v-col
        cols="4"
        class="py-2"
      >

        <v-text-field
          label="Select time period to consider"
          hint="Select the time to consider where pumping rate (Q) is varied and time (T) is constant"
          suffix="days"
          persistent-hint
          required>
        </v-text-field>
      </v-col>
      <v-col cols="6">
        <v-btn-toggle v-model="toggle_exclusive">
          <v-btn small>
            Latest time considered
          </v-btn>
          <v-btn small>
            Earliest time considered
          </v-btn>
        </v-btn-toggle>
      </v-col>
    </v-row>
    </v-card>
    <v-card class="mt-5 pa-5" outlined tile>
      <v-row>
        <v-col
          cols="4"
          class="py-2"
        >

          <v-text-field
            label="Select time period to consider"
            hint="Select the time to consider where pumping rate (Q) is varied and time (T) is constant"
            suffix="days"
            persistent-hint
            required>
          </v-text-field>
        </v-col>
        <v-col cols="6">
          <label class="pl-5">
            <input type="radio" name="radio" value="latest"/>
            Latest time considered
          </label>
          <label class="pl-5">
            <input type="radio" name="radio" value="earliest"/>
            Earliest time considered
          </label>
        </v-col>
      </v-row>
    </v-card>
  </v-form>
</template>
<script>

export default {
  name: 'TimePeriodToConsider',

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
