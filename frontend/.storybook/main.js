const path = require('path') // used for resolving aliases

module.exports = {
  'stories': [
    '../src/**/*.stories.mdx',
    '../src/**/*.stories.@(js|jsx|ts|tsx)'
  ],
  'addons': [
    '@storybook/addon-links', '@storybook/addon-essentials',
    '@storybook/preset-scss'
  ],

  // add this function to tweak the webpack config
  webpackFinal: async (config, { configType }) => {
    // `configType` has a value of 'DEVELOPMENT' or 'PRODUCTION'
    // You can change the configuration based on that.
    // 'PRODUCTION' is used when building the static version of storybook

    // so I can import { storyFactory } from '~storybook/util/helpers'
    // config.resolve.alias['~storybook'] = path.resolve(__dirname)
    // the @ alias points to the <code>src/</code> directory, a common alias
    // used in the Vue community
    config.resolve.alias['@'] = path.resolve(__dirname, '..', 'src')

    // config.module.rules.push({
    //   test: /\.sass$/,
    //   use: [
    //     'vue-style-loader',
    //     'css-loader',
    //     {
    //       loader: 'sass-loader',
    //       // Requires sass-loader@^7.0.0
    //       options: {
    //         // This is the path to your variables
    //         data: "@import '@/styles/variables.scss'"
    //       },
    //       // Requires sass-loader@^8.0.0
    //       options: {
    //         // This is the path to your variables
    //         prependData: "@import '@/styles/variables.scss'"
    //       },
    //       // Requires sass-loader@^9.0.0
    //       options: {
    //         // This is the path to your variables
    //         additionalData: "@import '@/styles/variables.scss'"
    //       },
    //     },
    //   ],
    // })

    // -- from https://morphatic.com/2020/09/30/configuring-storybook-6-for-vue-2-vuetify-2-3/
    // THIS is the tricky stuff!
    // config.module.rules.push({
    //   test: /\.sass$/,
    //   use: [
    //     'style-loader',
    //     'css-loader',
    //     {
    //       loader: 'sass-loader',
    //       options: {
    //         sassOptions: {
    //           indentedSyntax: true,
    //         },
    //         prependData: `@import '@/sass/variables.sass'`,
    //       },
    //     }
    //   ],
    //   include: path.resolve(__dirname, '../'),
    // })

    // config.module.rules.push({
    //   test: /\.scss$/,
    //   use: ['style-loader', 'css-loader', 'sass-loader'],
    //   include: path.resolve(__dirname, '../'),
    // });

    // return the updated Storybook configuration
    return config
  },
  // presets: [
  //   'vue/app'
  // ],
}
//   ],
//   presets: [
//     '@vue/app'
//   ],
// }
