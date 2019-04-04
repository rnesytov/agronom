var BundleTracker = require('webpack-bundle-tracker');
var address = require("address");

module.exports = {
    webpack: (config, env) => {

        config.plugins.push(
          new BundleTracker({
            path: __dirname,
            filename: "./build/webpack-stats.json",
            publicPath: "http://" + address.ip() + ":3000/"
          })
        );

        config.optimization.splitChunks.name = 'vendors';

        return config;
    },
};
