<template>
    <el-container>
        <el-header>  
            <div>
                <img src='' alt=''>
                <span>管理平台</span>
            </div>
                <el-button type='info' @click="logout">退出</el-button>
        </el-header>
    </el-container>
</template>

<style lang="less" scoped>
	@import '../style/mixin';
    .el-header{
        background-color: #244e92;
        display: flex;
        justify-content: space-between;
        padding-left: 20px;
        align-items: center;
        color: #ffffff;
        font-size: 16px;
        > div{
            display: flex;
            align-items: center;
            span{
                margin-left: 15px
            }
        }
    }
    .el-aside{
        background-color: #244e92;
    }
    .el-main{
        background-color: hsl(240, 8%, 83%);
    }
    .home-container{
        height: 70px;
    }
</style>