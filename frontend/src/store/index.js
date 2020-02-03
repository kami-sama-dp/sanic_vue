import Vue from 'vue'
import Vuex from 'vuex'
import * as types from "./types"

Vue.use(Vuex)

const state = {
   token: '',
}

const mutations = {
   set_token(state, token) {
      state.token = token
      localStorage.token = token
  },
  del_token(state) {
      state.token = ''
      localStorage.removeItem('token')
  }
}

const actions = {
}

 export default new Vuex.Store({
    state, 
    mutations,
    actions
})