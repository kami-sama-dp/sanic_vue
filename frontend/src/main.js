import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import routes from './router/index'
import store from './store'
import ElementUI, { MessageBox } from 'element-ui'
import axios from  'axios'
import 'element-ui/lib/theme-chalk/index.css'

Vue.prototype.$axios = axios
Vue.prototype.$confirm = MessageBox.confirm
Vue.config.productionTip = false



Vue.use(ElementUI)
Vue.use(VueRouter)

const router = new VueRouter({
  routes,
  mode: 'hash',
  strict: process.env.NODE_ENV !== 'production',
})

new Vue({
  render: h => h(App),
  router,
  store,
}).$mount('#app')