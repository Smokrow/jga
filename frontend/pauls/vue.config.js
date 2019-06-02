// vue.config.js
module.exports = {
  // options...
	devServer: {
		proxy: {
      '/api': {
	      target: 'http://192.168.178.38:5555',
        ws: true,
	changeOrigin: true,
      },}
  }

}
