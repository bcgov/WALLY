module.exports = {
  presets: [
    '@vue/app'
  ],
  env: {
    test: {
      plugins: ['dynamic-import-node-babel-7']
    }
  },
  sourceType: 'unambiguous'
}
