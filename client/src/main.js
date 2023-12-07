import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/vant.js'
import './plugins/md5.js'

import axios from 'axios'

Vue.prototype.$http = axios

// 配置请求根路径
axios.defaults.baseURL = process.env.VUE_APP_API_URL

axios.interceptors.request.use(config => {
    console.log(config)
    config.headers.Authorization = window.localStorage.getItem('token')
    return config
})

if (process.env.NODE_ENV === 'production') {
    console.log('部署环境')
} else if(process.env.NODE_ENV === 'development') {
    console.log('开发环境')
}

Vue.config.productionTip = false

new Vue({
    router,
    render: h => h(App)
}).$mount('#app')
