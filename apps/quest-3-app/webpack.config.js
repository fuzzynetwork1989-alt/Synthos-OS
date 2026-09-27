const path = require('path');

module.exports = {
  entry: './index.js',
  target: 'node',
  mode: process.env.NODE_ENV || 'development',
  
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
    clean: true
  },
  
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      }
    ]
  },
  
  resolve: {
    extensions: ['.js'],
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  },
  
  externals: {
    // Meta Spatial SDK would be external in production
    '@meta/spatial-sdk': 'commonjs @meta/spatial-sdk'
  },
  
  optimization: {
    minimize: true,
    usedExports: true
  }
};