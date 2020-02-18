module.exports = {
    devServer:{
        proxy:"http://localhost:8888/", //解决跨域问题
        overlay: {
            warnings: false,
            errors: false
        }
    },
    lintOnSave :false
}
