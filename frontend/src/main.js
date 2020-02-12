import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import routes from './router/index'
import store from './store'
import ElementUI, { MessageBox } from 'element-ui'
import axios from  './http'
import 'element-ui/lib/theme-chalk/index.css'
import VueScrollLock from 'vue-scroll-lock'

Vue.prototype.$axios = axios
Vue.prototype.$confirm = MessageBox.confirm

Vue.config.productionTip = false



Vue.use(ElementUI)
Vue.use(VueRouter)
Vue.use(VueScrollLock)

const router = new VueRouter({
  routes,
  mode: 'hash',
  strict: process.env.NODE_ENV !== 'production',
})


// // 页面刷新时，重新赋值token
// if (window.localStorage.getItem('token')) {
//   store.commit(set_token, window.localStorage.getItem('token'))
// }

//全局路由钩子
router.beforeEach((to, from, next) => {
  if (to.meta.requireAuth) {
      // 检查localStorage
      if (localStorage.token) {
          store.commit('set_token', {
            token: localStorage.token,
            user: localStorage.getItem('username')
          })
          // 添加axios头部Authorized
          axios.defaults.auth = {
              username: store.state.token,
              password: store.state.token,
          }
          next()
      } else {
          next({
              path: '/login',
          })
      }
  }
  else {
      next()
  }
})

new Vue({
  render: h => h(App),
  router,
  store,
  axios
}).$mount('#app')