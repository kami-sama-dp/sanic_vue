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
   set_master(state, data){
      state.master.push(data)
      localStorage.setItem('master', JSON.stringify(state.master))
   },
   set_slaves(state, data){
      state.slaves.push(data)
      localStorage.setItem('slaves', JSON.stringify(state.slaves))
   },
   remove_master(state){
      state.master = []
      localStorage.removeItem('master')
   },
   remove_slaves(state){
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