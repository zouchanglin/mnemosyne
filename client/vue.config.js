const { VantResolver } = require('@vant/auto-import-resolver')
const ComponentsPlugin = require('unplugin-vue-components/webpack')

module.exports = {
    configureWebpack: {
        plugins: [
            ComponentsPlugin({
                resolvers: [VantResolver()]
            })
        ]
    },
    devServer: {
        compress: true,
        disableHostCheck: true
    },
    css: {
        loaderOptions: {
            less: {
                lessOptions: {
                    modifyVars: {
                        // 直接覆盖变量
                        'nav-bar-background-color': '#3aa2ff',
                        'nav-bar-text-color': '#fff',
                        'nav-bar-title-text-color': '#fff'
                    }
                }
            }
        }
    }
}
