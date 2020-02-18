<template>
  <div class="fillcontain">
    <HeaderTopMain></HeaderTopMain>
    <el-card class="box-card" style="margin-top:18px;height:95%">
      <el-row :gutter="10">
        <el-col :span="7">
          <el-input
            placeholder="请输入内容"
            v-model.trim="search_task"
            @keyup.enter.native="search_data"
            clearable
            @clear="search_data"
          >
            <el-button slot="append" icon="el-icon-search" />
          </el-input>
        </el-col>
        <!-- <el-col :span="2">
          <el-button type="primary">搜索</el-button>
        </el-col>-->
        <el-col :span="3">
          <el-button type="primary" @click="showaddDialog">添加测试任务</el-button>
        </el-col>
      </el-row>

      <el-table
        :data="testTask"
        style="margin-top:18px;font-size:12px;width: 100%"
        border
        stripe
        height="86%"
        v-loading="loading"
      >
        <el-table-column label="#" width="80%" type="index" :index="indexMethod"></el-table-column>
        <el-table-column label="任务名称" prop="task_name" width="250%"></el-table-column>
        <el-table-column label="目标主机" prop="testhost" width="90%"></el-table-column>
        <el-table-column label="创建人" prop="user" width="90%"></el-table-column>
        <el-table-column label="运行时长" prop="runtime" width="90%"></el-table-column>
        <el-table-column label="自动停止" prop="autostop" width="90%">
          <template v-slot="scope">
            <el-tag :type="scope.row.autostop =='是'?'':'danger'">{{scope.row.autostop}}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="控制器" prop="master" width="140%">
          <template v-slot="scope">
            <el-tag>{{scope.row.master}}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="客户端列表" prop="slaves_name" width="200%">
          <template v-slot="scope">
            <el-tag
              v-for="(value, index) in scope.row.slaves_name"
              :key="index"
              style="margin-left: 5px;"
            >{{value}}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="客户端核心总数" prop="slaves_core_size" width="105%">
          <template v-slot="scope">
            <el-tag
              v-for="(value, index) in scope.row.slaves_core_size"
              :key="index"
              style="margin-left: 5px;"
            >{{value}}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="并发用户数" prop="usersize" width="90%"></el-table-column>
        <el-table-column label="每秒启动用户数" prop="userspeed" width="110%"></el-table-column>
        <el-table-column label="备注" prop="desc"></el-table-column>
        <el-table-column label="操作" width="190%">
          <template v-slot="scope">
            <el-button type="primary" icon="el-icon-edit" size="mini" @click="editTask(scope.row)"></el-button>
            <el-button
              type="danger"
              icon="el-icon-delete"
              size="mini"
              @click="removeTaskById(scope.row.id)"
            ></el-button>
            <el-button type="primary" icon="el-icon-caret-right" size="mini" @click="runTask(scope.row)"></el-button>
          </template>
        </el-table-column>
      </el-table>

      <!--分页区域-->
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="queryInfo.curPage"
        :page-sizes="[10, 20, 30, 50]"
        :page-size="queryInfo.pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        style="margin-top:15px"
      ></el-pagination>
    </el-card>
  </div>
</template>

<script>
import HeaderTopMain from "../components/HeaderTopMain";
export default {
  inject: ["reload"],
  components: {
    HeaderTopMain
  },
  data() {
    return {
      search_task: "",
      loading: false,
      testTask: [],
      total: 0,
      queryInfo: {
        task_name: "",
        curPage: 1,
        pageSize: 10
      }
    };
  },
  created() {
    this.getTaskList();
  },
  methods: {
    // 翻页，连续index索引
    indexMethod(index) {
      return index + 1 + (this.queryInfo.curPage - 1) * this.queryInfo.pageSize;
    },
    async search_data() {
      //搜索框查询, 后期可优化成实时搜索
      this.queryInfo.task_name = this.search_task;
      this.queryInfo.curPage = 1;
      await this.getTaskList();
    },
    showaddDialog() {
      this.reload(); //刷新页面
      this.$router.push("/addTask");
    },
    async getTaskList() {
      try {
        const res = await this.$axios.get("/api/test_task/", {
          params: this.queryInfo
        });
        if (res.status == 200) {
          this.total = res.data.total;
          this.testTask = [];
          res.data.result.forEach(item => {
            this.slave_tags = [];
            const table_item = {
              user: item.user,
              id: item.id,
              task_name: item.taskname,
              testhost: item.testhost,
              runtime: item.runtime,
              autostop: item.autostop == true ? "是" : "否",
              slaves: item.slaves,
              slaves_name: item.slaves_name.split(","),
              master: item.master,
              master_local_ip :item.master_local_ip,
              slave_local_ip :item.slave_local_ip,
              slaves_core_size: item.slaves_core_size.split(','),
              usersize: item.usersize,
              userspeed: item.userspeed,
              indextimes: item.indextimes,
              desc: item.desc
            };
            this.testTask.push(table_item);
          });
        }
      } catch (err) {
        this.$message.error("获取务器列表数据失败!");
      }
    },
    // 监听pageSize改变的事件
    handleSizeChange(pageSize) {
      this.queryInfo.pageSize = pageSize;
      this.getTaskList();
    },
    //监听页码值改变的事件
    handleCurrentChange(curPage) {
      this.queryInfo.curPage = curPage;
      this.getTaskList();
    },
    editTask(row) {
      this.reload(); //刷新页面
      this.$router.push({path:'/editTask',query:{data: window.btoa(window.encodeURIComponent(JSON.stringify(row)))}}); //对url后面的参数加密
    },
    //删除任务ById
    async removeTaskById(id) {
      const res = await this.$confirm("是否删除", "确认信息", {
        distinguishCancelAndClose: false,
        confirmButtonText: "确认",
        cancelButtonText: "取消"
      }).catch(err => err);
      if (res == "confirm") {
        let param = { id: id };
        const _delete = await this.$axios.delete("/api/test_task/", {
          data: param
        });
        if(_delete.status == 200){
          this.$message.success('删除成功')
          this.getTaskList()
        }
        else{
          this.$message.error('删除失败')
          return
        }
      } else if (res == "cancel") {
        return this.$message.info("已取消删除");
      }
    },
    //执行任务
    async runTask(row){
      console.log(row)
      try{
        // let data = {
        //   user_name:row.user,
        //   slaves_name: row.slaves_name,
        //   master: row.master,
        //   task_name: row.task_name,
        //   master_local_ip: item.master_local_ip,
        //   slave_local_ip: item.slave_local_ip,
        //   slaves_core_size: item.slaves_core_size
        // }
        const res = await this.$axios.post('/api/runTask/', row)
        console.log(res)
      }catch{
        this.$message.error('执行任务出错')
      }
      
    }
  }
};
</script>

<style lang="less" scoped>
</style>