<template>
  <div class="fillcontain">
    <HeaderTopMain></HeaderTopMain>
    <el-card style="margin-top:18px;height:95%">
      <el-row :gutter="10">
        <el-col :span="7">
          <el-input
            placeholder="根据测试任务名称搜索"
            v-model.trim="search_report"
            @keyup.enter.native="search_report_data"
            clearable
            @clear="search_report_data"
          >
            <el-button slot="append" icon="el-icon-search" @click="search_report_data" />
          </el-input>
        </el-col>
        <!-- <el-col :span="2">
          <el-button type="primary">搜索</el-button>
        </el-col>-->
      </el-row>

      <el-table
        :data="testReport"
        style="margin-top:18px;font-size:12px;width: 100%"
        border
        stripe
        height="86%"
        v-loading="loading"
      >
        <el-table-column label="#" width="80%" type="index" :index="indexMethod"></el-table-column>
        <!-- <el-table-column label="报告id" prop="reportid" width="250%"></el-table-column> -->
        <el-table-column label="报告名称" prop="reporttitle" width="300%">
          <template v-slot="scope">
            <el-input v-model="scope.row.reporttitle" placeholder></el-input>
          </template>
        </el-table-column>
        <el-table-column label="测试任务" prop="report_task_name"></el-table-column>
        <el-table-column label="创建人" prop="user"></el-table-column>
        <el-table-column label="创建时间" prop="report_created_time"></el-table-column>
        <el-table-column label="执行时间" prop="report_run_time"></el-table-column>
        <el-table-column label="结束时间" prop="report_end_time"></el-table-column>
        <el-table-column label="状态" prop="status">
          <template v-slot="scope">
            <el-tag v-if="scope.row.reportstatus=='SUCCESS'" type="success">执行完成</el-tag>
            <el-tag v-if="scope.row.reportstatus=='PENDING'">正在执行</el-tag>
            <el-tag v-if="scope.row.reportstatus=='FAILURE'" type="danger">执行出错</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template v-slot="scope">
            <el-button
              type="primary"
              icon="el-icon-edit"
              size="mini"
              @click="editReportTitle(scope.row)"
            ></el-button>
            <el-button
              type="primary"
              icon="el-icon-info"
              size="mini"
              @click="showReportDetail(scope.row)"
            ></el-button>
            <el-button
              type="danger"
              icon="el-icon-delete"
              size="mini"
              v-if="scope.row.reportstatus=='SUCCESS'"
              @click="removeReportById(scope.row)"
            ></el-button>
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
  components: {
    HeaderTopMain
  },
  inject: ["reload"],
  data() {
    return {
      num: "11",
      loading: true, //默认开启加载动画特效
      search_report: "",
      testReport: [],
      queryInfo: {
        report_task_name: "",
        curPage: 1,
        pageSize: 10
      },
      total: 0
    };
  },
  created() {
    this.getReportList();
  },
  methods: {
    // 翻页，连续index索引
    indexMethod(index) {
      return index + 1 + (this.queryInfo.curPage - 1) * this.queryInfo.pageSize;
    },
    async search_report_data() {
      //搜索框查询, 后期可优化成实时搜索
      this.queryInfo.report_task_name = this.search_report;
      this.queryInfo.curPage = 1;
      await this.getReportList();
    },
    // 获取数据
    async getReportList() {
      try {
        const res = await this.$axios.get("/api/reportList/", {
          params: this.queryInfo
        });
        this.total = res.data.total;
        this.testReport = [];
        res.data.result.forEach(item => {
          const table_item = {
            reportid: item.reportid,
            reporttitle: item.reporttitle,
            user: item.user,
            report_created_time: this.getUTCDateTime(item.report_created_time),
            report_run_time: item.report_run_time,
            report_end_time:
              item.report_end_time == null
                ? ""
                : this.getDateTime(item.report_end_time),
            report_task_name: item.report_task_name,
            reportstatus: item.reportstatus
          };
          this.testReport.push(table_item);
        });
        this.loading = false;
      } catch (err) {
        this.$message.error("获取报告列表数据失败");
      }
    },
    // 监听pageSize改变的事件
    handleSizeChange(pageSize) {
      this.queryInfo.pageSize = pageSize;
      this.getReportList();
    },
    //监听页码值改变的事件
    handleCurrentChange(curPage) {
      this.queryInfo.curPage = curPage;
      this.getReportList();
    },
    /* 获取日期时间格式*/
    getUTCDateTime(date) {
      date = new Date(date);
      var year = date.getUTCFullYear();
      var month = date.getUTCMonth() + 1;
      var day =
        date.getUTCDate() < 10 ? "0" + date.getUTCDate() : date.getUTCDate();
      var hh =
        date.getUTCHours() < 10 ? "0" + date.getUTCHours() : date.getUTCHours();
      var mm =
        date.getUTCMinutes() < 10
          ? "0" + date.getUTCMinutes()
          : date.getUTCMinutes();
      var ss =
        date.getUTCSeconds() < 10
          ? "0" + date.getUTCSeconds()
          : date.getUTCSeconds();
      return year + "-" + month + "-" + day + " " + hh + ":" + mm + ":" + ss;
    },
    getDateTime(date) {
      date = new Date(date);
      var year = date.getFullYear();
      var month = date.getMonth() + 1;
      var day = date.getDate() < 10 ? "0" + date.getDate() : date.getDate();
      var hh = date.getHours() < 10 ? "0" + date.getHours() : date.getHours();
      var mm =
        date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();
      var ss =
        date.getSeconds() < 10 ? "0" + date.getSeconds() : date.getSeconds();
      return year + "-" + month + "-" + day + " " + hh + ":" + mm + ":" + ss;
    },
    async showReportDetail(row) {
      if (row.reportstatus == "SUCCESS") {
        let data = {
          reportid: row.reportid,
          report_task_name: row.report_task_name
        };
        const res = await this.$axios.get("/api/report_detail/", {
          params: data
        });
        if (res.status == 200) {
          this.$router.push({
            path: "/reportDetail",
            query: {
              data: window.btoa(
                window.encodeURIComponent(JSON.stringify(res.data))
              )
            }
          }); //对url后面的参数加密}
        } else {
          this.$message.error("获取详细数据失败");
        }
      } else if (row.reportstatus == "FAILURE") {
        this.$message.error("执行出错没有报告");
      } else {
        this.$message.info("请等待任务执行完成");
      }
    },
    async removeReportById(row) {
      const res = await this.$confirm("是否删除?", "确认信息", {
        distinguishCancelAndClose: false,
        confirmButtonText: "确认",
        cancelButtonText: "取消"
      }).catch(err => err);
      if (res == "confirm") {
        let param = { reportid: row.reportid };
        const _delete = await this.$axios.delete("/api/report_detail/", {
          data: param
        });
        if (_delete.status == 200) {
          this.$message.success("成功删除");
          this.getReportList();
        } else {
          this.$message.error("删除失败");
        }
      } else if (res == "cancel") {
        return this.$message.info("已取消删除");
      }
    },
    async editReportTitle(row) {
      let data = JSON.stringify(row);
      const res = await this.$axios.put("/api/report_detail/", data);
      if (res.status == 200) {
        this.$message.success("编辑成功");
      } else {
        this.$message.error("编辑失败");
        return;
      }
    }
  }
};
</script>


<style lang="less" scoped>
.input_width {
  width: 50%;
}
</style>

<!--当最后一页只有一条数据时，删除后，不会自动跳转至前一页，而是仍然处在当前页 （添加数据也有类似问题）后期优化-->