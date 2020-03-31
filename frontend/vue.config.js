const CompressionPlugin = require('compression-webpack-plugin')
// const Visualizer = require('webpack-visualizer-plugin')

module.exports = {
  configureWebpack: {
    resolve: {
      alias: {
        'plotly.js': 'plotly.js/dist/plotly-basic.min.js'
      }
    },
    plugins: [
      new CompressionPlugin({
        filename: '[dir][name].gz[ext][query]'
      })
      // new Visualizer() # Creates a stats.html file with a sunburst chart
    ]
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
