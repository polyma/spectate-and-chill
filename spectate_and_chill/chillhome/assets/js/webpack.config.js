var config = {
   entry: './main.jsx',

   output: {
      path:'./',
      filename: '../../static/bundle.js',
   },

   module: {
      loaders: [
         {
            test: /\.jsx?$/,
            exclude: /node_modules/,
            loader: 'babel',

            query: {
               presets: ['es2015', 'react']
            }
         }
      ]
   }
}

module.exports = config;
