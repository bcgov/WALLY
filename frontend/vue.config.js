const CompressionPlugin = require('compression-webpack-plugin')
module.exports = {
  configureWebpack: {
    resolve: {
      alias: {
        'plotly.js': 'plotly.js/dist/plotly-basic.min.js'
      }
    },
    plugins: [new CompressionPlugin({
      filename: '[dir][name].gz[ext][query]'
    })]
  }
}

// Start the bundle analyzer server
// const BundleAnalyzerPlugin = require('webpack-bundle-analyzer')
//   .BundleAnalyzerPlugin
// module.exports = {
//   configureWebpack: {
//     plugins: [new BundleAnalyzerPlugin()]
//   }
// }
