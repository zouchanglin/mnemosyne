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
    }
    // css: {
    //     loaderOptions: {
    //         less: {
    //             // 若 less-loader 版本小于 6.0，请移除 lessOptions 这一级，直接配置选项。
    //             modifyVars: {
    //                 // 直接覆盖变量
    //                 '@nav-bar-background-color': '#000'
    //             }
    //         }
    //     }
    // }
}
