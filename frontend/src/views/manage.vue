<template>
  <div class="fillcontain" >
    <el-container style="height:100%">
      <el-aside width="200px">
        <el-aside width="200px">
          <el-menu
            background-color="#001529"
            text-color="#fff"
            active-text-color="#409BFF"
            :unique-opened="true"
            :router="true"
            :default-active="defaultActive"
          >
            <el-menu-item index="home">
              <i class="el-icon-menu"></i>
              <span slot="title">首页</span>
            </el-menu-item>
            <!--一级菜单-->
            <!-- <el-submenu index="1"> -->
            <!--一级菜单模板区-->
            <!-- <template slot="title">
              <i class="el-icon-location"></i>
              <span>导航一</span>
            </template>-->
            <!--二级菜单-->
            <el-menu-item index="serverMachine">
              <i class="el-icon-location"></i>
              <span>服务器列表</span>
            </el-menu-item>

            <!-- <el-submenu index="2"> -->
            <!--一级菜单模板区-->
            <!-- <template slot="title">
              <i class="el-icon-location"></i>
              <span>导航二</span>
            </template>-->
            <!--二级菜单-->
            <el-menu-item index="testTask">
              <i class="el-icon-location"></i>
              <span>测试任务</span>
            </el-menu-item>
            <!-- </el-submenu> -->
            <!-- <el-submenu index="3"> -->
            <!--一级菜单模板区-->
            <!-- <template slot="title">
              <i class="el-icon-location"></i>
              <span>导航三</span>
            </template>-->
            <!--二级菜单-->
            <el-menu-item index="testReport">
              <i class="el-icon-location"></i>
              <span>测试报告</span>
            </el-menu-item>
            <!-- </el-submenu> -->
            <!-- <el-menu-item index="dataAnalysis">
              <i class="el-icon-location"></i>
              <span slot="title">数据分析</span>
            </el-menu-item> -->
          </el-menu>
        </el-aside>
      </el-aside>
      <el-container>
        <DbHeader></DbHeader>
        <el-main>
          <keep-alive>
            <router-view></router-view>
            <!--子路由在这里显示-->
          </keep-alive>
        </el-main>
        <el-footer style="padding:25px"></el-footer>
      </el-container>
    </el-container>
  </div>
</template>



<script>
import DbHeader from "../components/DbHeader";
export default {
  components: {
    DbHeader,
  },
  computed: {
    defaultActive: function() {
      return this.$route.path.replace("/", "");
    }
  }
};
</script>

<style lang="less" scoped>
.el-aside {
  background-color: #001529;
  .el-menu {
    border-right: none;
  }
}
.el-main {
  height: 100%;
}
</style>
