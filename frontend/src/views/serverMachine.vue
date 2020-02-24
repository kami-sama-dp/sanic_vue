<template>
  <div class="fillcontain">
    <HeaderTopMain></HeaderTopMain>
    <el-card style="margin-top:18px;height:95%">
      <el-row :gutter="10">
        <el-col :span="7">
          <el-input
            placeholder="根据服务器地址搜索"
            v-model.trim="seachIp"
            @keyup.enter.native="search_ip_data"
            clearable
            @clear="search_ip_data"
          >
            <el-button slot="append" icon="el-icon-search" @click="search_ip_data" />
          </el-input>
        </el-col>
        <!-- <el-col :span="2">
          <el-button type="primary">搜索</el-button>
        </el-col>-->
        <el-col :span="3">
          <el-button type="primary" @click="showaddDialog">添加服务器</el-button>
        </el-col>
      </el-row>
      <!--弹出框-->
      <el-dialog
        :title="titleMap[dialogTitle]"
        :visible.sync="dialogFormVisible"
        :close-on-click-modal="false"
        @close="closeDialog('machineRef')"
        :destroy-on-close="true"
      >
        <el-form :model="form" ref="machineRef" :rules="addMachineRules">
          <el-form-item label="服务器地址:" :label-width="formLabelWidth" prop="ip">
            <el-input v-model="form.ip" class="input_width" prop></el-input>
          </el-form-item>
          <el-form-item label="内网地址:" :label-width="formLabelWidth" prop="local_ip">
            <el-input v-model="form.local_ip" class="input_width" prop></el-input>
          </el-form-item>
          <el-form-item label="服务器端口:" :label-width="formLabelWidth" prop="port">
            <el-input v-model="form.port" class="input_width"></el-input>
          </el-form-item>
          <el-form-item label="核心数量:" :label-width="formLabelWidth" prop="coresize">
            <el-input v-model="form.coresize" class="input_width"></el-input>
          </el-form-item>
          <el-form-item label="控制器:" :label-width="formLabelWidth" prop="mtype">
            <el-radio v-model="form.mtype" :label="true">是</el-radio>
            <el-radio v-model="form.mtype" :label="false">否</el-radio>
          </el-form-item>
          <el-form-item label="备注:" :label-width="formLabelWidth" prop="desc">
            <el-input type="textarea" :rows="5" v-model="form.desc" class="input_width"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="cancelOff('machineRef')">取 消</el-button>
          <el-button type="primary" @click="addMachine('machineRef')">确 定</el-button>
        </div>
      </el-dialog>
      <el-table
        :data="serverMachine"
        style="margin-top:18px;font-size:12px;width: 100%"
        border
        stripe
        height="86%"
        v-loading="loading"
      >
        <el-table-column label="#" width="80%" type="index" :index="indexMethod"></el-table-column>
        <el-table-column label="服务器地址" prop="ip"></el-table-column>
        <!-- <el-table-column label="内网地址" prop="local_ip"></el-table-column> -->
        <el-table-column label="服务器端口" prop="port"></el-table-column>
        <el-table-column label="核心数量" prop="coresize"></el-table-column>
        <el-table-column label="控制器" prop="mtype" width="90%">
          <template v-slot="scope">
            <el-tag :type="scope.row.mtype =='是'?'':'danger'">{{scope.row.mtype}}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="备注" prop="desc"></el-table-column>
        <el-table-column label="操作">
          <template v-slot="scope">
            <el-button
              type="primary"
              icon="el-icon-edit"
              size="mini"
              @click="editShowDialog(scope.row)"
            ></el-button>
            <el-button
              type="danger"
              icon="el-icon-delete"
              size="mini"
              @click="removeMachineById(scope.row)"
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
    //自定义校验规则
    var checkIp = (rule, value, callback) => {
      var regIp = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
      if (regIp.test(value)) {
        return callback();
      } else {
        callback(new Error("请输入合法的ip"));
      }
    };
    var checkcoreSize = (rule, value, callback) => {
      var regcoreSize = /^\+?[1-9][0-9]*$/;
      if (regcoreSize.test(value)) {
        return callback();
      } else {
        callback(new Error("请输入大于0的整数"));
      }
    };
    return {
      loading: true, //默认开启加载动画特效
      seachIp: "",
      dialogTitle: "",
      titleMap: {
        showaddDialog: "添加服务器",
        showeditDialog: "修改服务器"
      },
      serverMachine: [],
      form: {
        id: 0,
        ip: "",
        local_ip: "",
        port: "22",
        coresize: "",
        mtype: false,
        desc: ""
      },
      dialogFormVisible: false,
      formLabelWidth: "120px",
      queryInfo: {
        ip: "",
        curPage: 1,
        pageSize: 10
      },
      total: 0,
      addMachineRules: {
        ip: [
          { required: true, message: "请输入地址", trigger: "blur" },
          { validator: checkIp }
        ],
        local_ip: [
          { required: true, message: "请输入地址", trigger: "blur" },
          { validator: checkIp }
        ],
        port: [{ required: true, message: "请输入端口", trigger: "blur" }],
        coresize: [
          { required: true, message: "请输入核心数量", trigger: "blur" },
          { validator: checkcoreSize }
        ]
      }
    };
  },
  created() {
    this.getMachineList();
  },
  methods: {
    // 翻页，连续index索引
    indexMethod(index) {
      return index + 1 + (this.queryInfo.curPage - 1) * this.queryInfo.pageSize;
    },
    async search_ip_data() {
      //搜索框查询, 后期可优化成实时搜索
      this.queryInfo.ip = this.seachIp;
      this.queryInfo.curPage = 1;
      await this.getMachineList();
    },
    closeDialog(refName) {
      this.form = {
        id: 0,
        ip: "",
        local_ip: "",
        port: "22",
        coresize: "",
        mtype: false,
        desc: ""
      };

      this.$refs[refName].resetFields();

      this.dialogFormVisible = false;
    },
    showaddDialog() {
      this.dialogTitle = "showaddDialog";
      this.dialogFormVisible = true;
    },
    // 将数据显示在弹出的编辑框
    async editShowDialog(row) {
      this.dialogTitle = "showeditDialog";
      this.form.id = row.id;
      this.form.local_ip = row.local_ip;
      this.form.ip = row.ip;
      this.form.port = row.port;
      this.form.coresize = row.coresize;
      this.form.mtype = row.mtype == "是" ? true : false;
      this.form.desc = row.desc;
      this.dialogFormVisible = true;
    },
    // 获取数据
    async getMachineList() {
      try {
        const res = await this.$axios.get("/api/machine/", {
          params: this.queryInfo
        });
        if (res.status == 200) {
          // this.$store.commit("remove_master")
          // this.$store.commit("remove_slaves")
          this.total = res.data.total;
          // 直接清库导致本地存储数据还在, 此时清空一下,保持数据一致性
          if (this.total == 0) {
            this.$store.commit("remove_master");
            this.$store.commit("remove_slaves");
          }
          this.serverMachine = [];
          res.data.result.forEach(item => {
            const table_item = {
              id: item.id,
              ip: item.ip,
              local_ip: item.local_ip,
              port: item.port,
              coresize: item.coresize,
              mtype: item.mtype == true ? "是" : "否",
              desc: item.desc
            };
            if (table_item.mtype == "是") {
              this.$store.commit("set_master", {
                id: table_item.id,
                ip: table_item.ip
                //   local_ip: item.local_ip
              });
            } else {
              this.$store.commit("set_slaves", {
                id: table_item.id,
                ip: table_item.ip
              });
            }
            this.serverMachine.push(table_item);
          });
          this.loading = false; //关闭加载动画特效
        } else {
          return;
        }
      } catch (err) {
        this.$message.error("获取务器列表数据失败");
      }
    },
    //点击确定按钮,添加数据或修改数据
    async addMachine(refName) {
      this.$refs[refName].validate(async valid => {
        if (!valid) {
          this.$message.error("格式有误");
          return;
        } else if (this.dialogTitle == "showeditDialog") {
          this.$store.commit("remove_master");
          this.$store.commit("remove_slaves");
          this.loading = true;
          let formData = JSON.stringify(this.form);
          this.dialogFormVisible = false;
          const res = await this.$axios.put("/api/machine/", formData);
          if (res.status == 200) {
            this.$message.success("编辑成功");
            this.getMachineList();
          } else {
            return;
          }
        } else if (this.dialogTitle == "showaddDialog") {
          this.loading = true;
          let formData = JSON.stringify(this.form);
          this.dialogFormVisible = false;
          const res = await this.$axios.post("/api/machine/", formData);
          if (res.status == 200) {
            this.$message.success("添加成功");
            //  this.reload(); // 刷新页面,此时会回到第一页（实际）， 而不是在当前页面刷新（预期）， 此问题未解决
            this.getMachineList(); //  刷新页面的另一种处理方式
            // this.loading = false; //关闭加载动画特效
          } else {
            return;
          }
        }
      });
      this.$refs[refName].resetFields();
      this.dialogFormVisible = false;
    },
    async removeMachineById(row) {
      const res = await this.$confirm("是否删除?", "确认信息", {
        distinguishCancelAndClose: false,
        confirmButtonText: "确认",
        cancelButtonText: "取消"
      }).catch(err => err);
      if (res == "confirm") {
        this.$store.commit("remove_master");
        this.$store.commit("remove_slaves");
        let param = { id: row.id };
        const _delete = await this.$axios.delete("/api/machine/", {
          data: param
        });
        if (_delete.status == 200) {
          this.$message.success("删除成功");
          this.getMachineList();
        } else {
          this.$message.error("删除失败");
          return;
        }
      } else if (res == "cancel") {
        return this.$message.info("已取消删除");
      }
    },
    // 取消按钮, 清空表单数据
    async cancelOff(refName) {
      this.form = {
        id: 0,
        ip: "",
        local_ip: "",
        port: "22",
        coresize: "",
        mtype: false,
        desc: ""
      };
      this.$refs[refName].resetFields();
      this.dialogFormVisible = false;
    },
    // 监听pageSize改变的事件
    handleSizeChange(pageSize) {
      this.queryInfo.pageSize = pageSize;
      this.getMachineList();
    },
    //监听页码值改变的事件
    handleCurrentChange(curPage) {
      this.queryInfo.curPage = curPage;
      this.getMachineList();
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