module.exports = {
    devServer:{
        proxy:'http:// 127.0.0.1:8888/', //解决跨域问题
        overlay: {
            warnings: false,
            errors: false
        }
    },
    lintOnSave :false
}
