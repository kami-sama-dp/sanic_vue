import axios from 'axios'
import router from './router'
import store from './store/index'
import { MessageBox, Notification} from 'element-ui';
import iView from 'iview'
import "iview/dist/styles/iview.css"

// axios 配置
axios.defaults.timeout = 6000
axios.defaults.auth = {
    username: '',
    password: '',
}
axios.interceptors.request.use(config=>{
    iView.LoadingBar.start();
    return config
}, 
    err=>{
        iView.LoadingBar.error();
        return Promise.reject(error)
})



//响应拦截器
axios.interceptors.response.use(response =>{
    iView.LoadingBar.finish();
    return response
},err=>{
    iView.LoadingBar.error();
    console.log(err.response) ;
    if (err.response){
        switch(err.response.status){
            case 403:
                Notification({
                    title: '密码错误',
                    offset: 80,
                    type: 'error',
                    duration: 3000,
                })
                store.commit('del_token')
                break;
            case 401:  
                store.commit('del_token')
                MessageBox.alert('用户登录信息已过期,请重新登录','提示',{
                    confirmButtonTest:'确定',
                    callback: action =>{
                        window.location.reload()
                    }
                })
                break;
            default:
                Notification.error({
                    title: '错误',
                    message: '未知错误',
                    duration: 5000,
                });
            return err;
        }
    }
    return Promise.reject(err.response).catch(err=>{return err})
})

export default axios