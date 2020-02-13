import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
   token: '',
   user: '',
   master: [],
   slaves: [],
}

const mutations = {
   set_token(state, data) {
      state.token = data.token
      state.user = data.user
      localStorage.token = data.token
      localStorage.setItem('username', data.user)
   },
   del_token(state) {
      state.token = ''
      state.user = ''
      localStorage.removeItem('token')
      localStorage.removeItem('username')
   },
   set_master(state, data) {
      // 去重
      if (state.master.length == 0) { 
         state.master.push(data)
         localStorage.setItem('master', JSON.stringify(state.master))
       }
      else if (JSON.stringify(state.master).indexOf(JSON.stringify(data)) == -1) {
         state.master.push(data)
         localStorage.setItem('master', JSON.stringify(state.master))
      }
   },
   set_slaves(state, data) {
      // 去重
      if (state.slaves.length == 0) { 
         state.slaves.push(data)
         localStorage.setItem('slaves', JSON.stringify(state.slaves))
       }
      else if (JSON.stringify(state.slaves).indexOf(JSON.stringify(data)) == -1) {
         state.slaves.push(data)
         localStorage.setItem('slaves', JSON.stringify(state.slaves))
      }

   },
   remove_master(state) {
      state.master = []
      localStorage.removeItem('master')
   },
   remove_slaves(state) {
      state.slaves = []
      localStorage.removeItem('slaves')
   }
}

const actions = {
}

export default new Vuex.Store({
   state,
   mutations,
   actions
})