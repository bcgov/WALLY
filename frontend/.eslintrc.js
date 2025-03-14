module.exports = {
  root: true,
  env: {
    node: true
  },
  extends: [
    'plugin:vue/essential',
    '@vue/standard'
  ],
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'vue/multi-word-component-names': process.env.NODE_ENV === 'production' ? 'off' : 'warn',
    'vue/valid-v-slot': ["error", {
      'allowModifiers': true
    }]
  },
  parserOptions: {
    parser: '@babel/eslint-parser'
  }
}
