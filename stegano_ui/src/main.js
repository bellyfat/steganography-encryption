import Vue from 'vue'
import App from './App.vue'
import router from './router'
import VueAxios from 'vue-axios'
import VueAuthenticate from 'vue-authenticate'
import axios from 'axios'

import './plugins/element.js'
import 'element-ui/lib/theme-chalk/display.css'

let API_ENDPOINT = process.env.VUE_APP_API_ENDPOINT
axios.defaults.headers.post['Content-Type'] = 'application/json'
axios.defaults.baseURL = API_ENDPOINT
Vue.use(VueAxios, axios)
Vue.use(VueAuthenticate, {
  baseUrl: API_ENDPOINT,
  tokenName: 'access_token',
  storageType: 'cookieStorage'
})

Vue.config.productionTip = false
new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
